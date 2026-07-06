// Manual test driver — the ONLY executable on the C++ side for now, which
// makes it your component's living proof. Build:
//   g++ -std=c++17 -Iinclude -Ilib src/VectorStore.cpp tests/test_vectorstore.cpp -o test_vs
//
// STUDY BANK — this file
// - Why does main() live HERE and not in VectorStore.cpp? (One sentence.
//   If you can't produce it, revisit "multiple definition of main".)
// - Exit codes: `return 1` on failure is what makes this driver usable in
//   scripts/CI later. -> look up: "process exit code convention"
// - assert vs if+print: <cassert> is the quick tool; know its gotcha
//   (-DNDEBUG silently removes asserts in release builds).
#include <iostream>
#include "VectorStore.h"

int main() {
    // CHECKPOINT 1 — cosine anchor (unlocks after Step 1 of the guide)
    // TODO(you): call cosine on {1,2,3} vs {4,5,6}; print; expect ~0.9746.
    // Note: it's private. THINK: temporary public? public test wrapper?
    // Or trust that Checkpoint 3 exercises it through search()? Each is
    // defensible — pick one and know why. ("friend" also exists; look it
    // up, decide if it's overkill here. It probably is.)

    // CHECKPOINT 2 — loader (unlocks after Step 3)
    VectorStore store;
    if (!store.load_from_jsonl("output/chunks.jsonl")) {   // fix path to yours
        std::cerr << "load failed\n";
        return 1;
    }
    std::cout << "chunks=" << store.size()
              << " dim=" << store.dimension() << "\n";
    // Expected with ingestion's sample PDF: chunks=17, dim=384.

    // CHECKPOINT 3 — self-retrieval property test (unlocks after Step 4)
    // THE IDEA: a vector's angle to itself is 0 -> cosine ~1.0 -> querying
    // with chunk i's OWN embedding must return chunk i at rank 1.
    // This one test proves loader + math + scoring + sort direction +
    // top-k packaging simultaneously, with no C++ embedder needed.
    // TODO(you): for a few i (0, 5, 16): search(storage-of-i's embedding, 3)
    //   - assert top result IS chunk i (match on chunk identity — think:
    //     how do you check that from a SearchResult? text equality? add
    //     chunk_index to SearchResult? DECIDE — tiny contract choice, yours)
    //   - assert its score > 0.999
    //   - print top-3 as: score | source_document | p.page | text[:80]
    //   - READ the #2/#3 results: overlapping neighbor chunks should rank
    //     high. That's semantic retrieval visibly working. Enjoy it.

    return 0;
}
