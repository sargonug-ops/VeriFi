// Benchmark harness for VectorStore — not part of the unit tests.
// Measures load_from_jsonl() throughput and search() latency/throughput
// across dataset sizes, using synthetic (random) 384-dim embeddings.
//
// Build:
//   clang++ -std=c++17 -O2 -Iinclude -Ilib \
//     src/VectorStore.cpp tests/bench_vectorstore.cpp -o bench_vectorstore
// Run:
//   ./bench_vectorstore [scratch_dir]
//
// scratch_dir is where synthetic .jsonl fixtures are written (defaults to
// /tmp/verifi_bench); it is not part of the repo's data.

#include "VectorStore.h"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <fstream>
#include <numeric>
#include <random>
#include <string>
#include <sys/stat.h>
#include <vector>

namespace {

constexpr int kDim = 384;

std::string make_dir(const std::string& base) {
    mkdir(base.c_str(), 0755);
    return base;
}

// Writes `num_chunks` synthetic records matching ingestion's JSONL schema.
// Each chunk's text encodes its own index so search() results can be
// matched back to ground truth without needing chunk_index on SearchResult.
void write_synthetic_jsonl(const std::string& path, int num_chunks, unsigned seed) {
    std::ofstream out(path, std::ios::binary);
    std::mt19937 rng(seed);
    std::uniform_real_distribution<float> dist(-1.0f, 1.0f);

    for (int i = 0; i < num_chunks; ++i) {
        out << "{\"chunk_index\":" << i
            << ",\"text\":\"synthetic_chunk_" << i << "\""
            << ",\"source_document\":\"synthetic_doc.pdf\""
            << ",\"page_number\":" << (i % 50 + 1)
            << ",\"embedding\":[";
        for (int d = 0; d < kDim; ++d) {
            if (d) out << ',';
            out << dist(rng);
        }
        out << "]}\n";
    }
}

double percentile(std::vector<double> sorted_us, double pct) {
    if (sorted_us.empty()) return 0.0;
    std::size_t idx = static_cast<std::size_t>(pct * (sorted_us.size() - 1));
    return sorted_us[idx];
}

struct SearchStats {
    double mean_us, p50_us, p90_us, p99_us, qps;
};

SearchStats time_searches(const VectorStore& store,
                           const std::vector<std::vector<float>>& queries,
                           int top_k) {
    std::vector<double> latencies_us;
    latencies_us.reserve(queries.size());

    auto t_total_start = std::chrono::steady_clock::now();
    for (const auto& q : queries) {
        auto t0 = std::chrono::steady_clock::now();
        auto results = store.search(q, top_k);
        auto t1 = std::chrono::steady_clock::now();
        latencies_us.push_back(
            std::chrono::duration<double, std::micro>(t1 - t0).count());
        if (results.empty()) std::printf("  (warning: empty result set)\n");
    }
    auto t_total_end = std::chrono::steady_clock::now();
    double total_s =
        std::chrono::duration<double>(t_total_end - t_total_start).count();

    std::sort(latencies_us.begin(), latencies_us.end());
    double mean = std::accumulate(latencies_us.begin(), latencies_us.end(), 0.0) /
                  latencies_us.size();

    return SearchStats{mean,
                        percentile(latencies_us, 0.50),
                        percentile(latencies_us, 0.90),
                        percentile(latencies_us, 0.99),
                        queries.size() / total_s};
}

bool run_correctness_check(const std::string& scratch_dir) {
    std::string path = scratch_dir + "/correctness.jsonl";
    constexpr int kN = 500;
    write_synthetic_jsonl(path, kN, /*seed=*/1);

    VectorStore store;
    if (!store.load_from_jsonl(path)) {
        std::printf("[correctness] FAIL: load_from_jsonl failed\n");
        return false;
    }
    if (store.fetchSize() != kN || store.dimension() != kDim) {
        std::printf("[correctness] FAIL: fetchSize=%zu dimension=%d (expected %d/%d)\n",
                    store.fetchSize(), store.dimension(), kN, kDim);
        return false;
    }

    // Self-retrieval property test: querying with chunk i's own embedding
    // must return chunk i at rank 1 with score ~1.0. Re-derive the same
    // embeddings deterministically (same seed) to get a query vector.
    std::mt19937 rng(1);
    std::uniform_real_distribution<float> dist(-1.0f, 1.0f);
    std::vector<std::vector<float>> embeddings(kN, std::vector<float>(kDim));
    for (int i = 0; i < kN; ++i) {
        // must match write_synthetic_jsonl's generation order exactly
        for (int d = 0; d < kDim; ++d) embeddings[i][d] = dist(rng);
    }

    bool ok = true;
    for (int i : {0, 5, 250, 499}) {
        auto results = store.search(embeddings[i], 3);
        std::string expected_text = "synthetic_chunk_" + std::to_string(i);
        if (results.empty() || results[0].text != expected_text || results[0].score < 0.999f) {
            std::printf("[correctness] FAIL at i=%d: top result='%s' score=%f\n",
                        i, results.empty() ? "<empty>" : results[0].text.c_str(),
                        results.empty() ? 0.0f : results[0].score);
            ok = false;
        }
    }
    if (ok) std::printf("[correctness] PASS: self-retrieval holds, dimension=%d\n\n", store.dimension());
    return ok;
}

}  // namespace

int main(int argc, char** argv) {
    std::string scratch_dir = argc > 1 ? argv[1] : "/tmp/verifi_bench";
    make_dir(scratch_dir);

    if (!run_correctness_check(scratch_dir)) {
        std::printf("Correctness check failed; aborting benchmark.\n");
        return 1;
    }

    const std::vector<int> sizes = {1000, 10000, 100000, 250000};
    constexpr int kNumQueries = 300;
    const std::vector<int> top_ks = {10, 50};

    std::printf("%-10s %-14s %-16s %-6s %-9s %-9s %-9s %-9s %-10s\n",
                "chunks", "load_ms", "chunks/sec", "top_k", "p50(us)",
                "p90(us)", "p99(us)", "mean(us)", "queries/sec");
    std::printf("--------------------------------------------------------------------------------------\n");

    for (int n : sizes) {
        std::string path = scratch_dir + "/chunks_" + std::to_string(n) + ".jsonl";
        write_synthetic_jsonl(path, n, /*seed=*/42);

        VectorStore store;
        auto t0 = std::chrono::steady_clock::now();
        bool loaded = store.load_from_jsonl(path);
        auto t1 = std::chrono::steady_clock::now();
        double load_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

        if (!loaded) {
            std::printf("load_from_jsonl failed for n=%d\n", n);
            continue;
        }

        double chunks_per_sec = n / (load_ms / 1000.0);

        std::mt19937 rng(7);
        std::uniform_real_distribution<float> dist(-1.0f, 1.0f);
        std::vector<std::vector<float>> queries(kNumQueries, std::vector<float>(kDim));
        for (auto& q : queries)
            for (auto& v : q) v = dist(rng);

        for (int top_k : top_ks) {
            SearchStats stats = time_searches(store, queries, top_k);
            std::printf("%-10d %-14.2f %-16.0f %-6d %-9.1f %-9.1f %-9.1f %-9.1f %-10.1f\n",
                        n, load_ms, chunks_per_sec, top_k, stats.p50_us,
                        stats.p90_us, stats.p99_us, stats.mean_us, stats.qps);
        }
    }

    std::printf("\nNote: search() is a brute-force O(n) scan over all stored\n"
                "embeddings per query, so latency scales ~linearly with corpus size\n"
                "regardless of top_k.\n");

    return 0;
}
