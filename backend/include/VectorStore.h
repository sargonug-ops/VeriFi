#pragma once
#include <string>
#include <vector>
#include "DocumentChunk.h"

/* ============================================================================
   STUDY BANK — this file
   ----------------------------------------------------------------------------
   1. Class declaration vs definition: this header PROMISES these functions
      exist; VectorStore.cpp DELIVERS them. The linker matches promises to
      deliveries. -> look up: "declaration vs definition C++",
      "undefined reference to" (read one StackOverflow answer on it NOW,
      before you cause it — you will cause it).
   2. const member functions — the trailing `const` on search() and
      cosine_similarity(). What does it promise? Why does the COMPILER
      enforce it? -> look up: "const member function c++"
   3. Pass by const reference: `const std::vector<float>&`. Three-part
      question to answer for yourself: what does `&` avoid, what does
      `const` forbid, and what would passing by value cost for 384 floats
      called N times per query?
   4. public vs private: why is cosine_similarity private? Who is the
      "public" here? (Answer in one sentence: the bridge/binding sees
      load + search + size + dimension, and NOTHING else.)
   5. Default member initializers: `int expected_dim_ = 384;` — when does
      this assignment happen? -> look up: "in-class member initializer"
   ============================================================================ */

// In-memory exact cosine-similarity k-NN store.
// Transport-agnostic on purpose: no HTTP, no networking, no JSON types in
// this interface — callers hand in plain C++ values and get plain C++ back.
class VectorStore {
public:
    VectorStore() = default;
    // THINK ABOUT: what does `= default` mean, and why is it enough here?
    // (What would you need a custom constructor FOR, and do you have that
    //  need?) -> look up: "rule of zero c++"

    /* ------------------------------------------------------------------
       STUDY BANK — load_from_jsonl (Phase 1: runs once at startup)
       ------------------------------------------------------------------
       Functions/tools to study:
       - std::ifstream            (open a file; how do you test it opened?)
       - std::getline             (read ONE line; what's its loop idiom?)
       - nlohmann::json::parse    (string -> json object; THROWS on bad input)
       - j["field"].get<T>()      (typed extraction; works for
                                   std::vector<float> directly!)
       - try / catch              (what is std::exception::what()?)
       - storage.push_back / storage.reserve
       Concepts:
       - JSONL vs JSON: why must you parse per-LINE, never the whole file?
       - RAII: why is there no file.close() in modern C++ code?
       Decisions YOU must make (comment your choice + why, in the code):
       - A line's embedding.size() != expected_dim_: reject whole file,
         or skip line + count skips? What does each mean for debugging?
       - json::parse throws on a malformed line: crash loudly (fine in
         dev) or catch-and-skip? Make it a CHOICE, not an accident.
       ------------------------------------------------------------------ */
    bool load_from_jsonl(const std::string& filepath);

    /* ------------------------------------------------------------------
       STUDY BANK — search (Phase 2: runs per query; the hot path)
       ------------------------------------------------------------------
       Functions/tools to study:
       - std::sort (in <algorithm>) with a CUSTOM COMPARATOR lambda
         -> look up: "std::sort custom comparator lambda descending"
         This is THE new concept of this function. Budget real time here.
       - std::pair<float, size_t>  (why score FIRST? what does pair's
         default operator< compare first? test your guess!)
       - std::min                  (for min(top_k, N) — edge: top_k > N)
       - .reserve()                (you know N up front — use it. Why?)
       Concepts:
       - Why sort {score, index} pairs instead of {score, DocumentChunk}?
         Reason it out in terms of what gets COPIED during a sort's swaps.
       - Guard clauses: the empty/invalid cases return early. List every
         way a caller could hand you garbage: empty store? k <= 0?
         query.size() != 384? Handle each BEFORE the loop.
       Complexity honesty (for your own understanding + the resume):
       - Scoring is O(N·d). Full sort is O(N log N). Name it what it is.
       - std::partial_sort / heap gets O(N log k) — that is a LATER,
         MEASURED upgrade. Do not build it in v1.
       ------------------------------------------------------------------ */
    std::vector<SearchResult> search(const std::vector<float>& query_embedding,
                                     int top_k) const;

    /* ------------------------------------------------------------------
       STUDY BANK — the two one-liners
       - size_t vs int for sizes -> look up: "why size_t"
       - These exist so the TEST DRIVER can verify loading. Trivial code,
         real purpose: observability.
       ------------------------------------------------------------------ */
    size_t size() const;
    int dimension() const;

private:
    /* ------------------------------------------------------------------
       STUDY BANK — cosine_similarity (the math core; write this FIRST)
       ------------------------------------------------------------------
       Functions to study:
       - std::sqrt (in <cmath>)
       - (optional, AFTER a manual version works) std::inner_product in
         <numeric> — compare it to your hand-rolled loop.
       Math to be able to derive on paper before typing:
       - dot(a,b) = sum over i of a[i]*b[i]
       - |a| = sqrt(sum of a[i]^2)
       - cosine = dot / (|a| * |b|)
       - WHY does this measure semantic similarity? One sentence about
         angles between vectors. If you can't write that sentence, read
         about cosine similarity for 10 more minutes.
       Edge case YOU must decide:
       - magnitude == 0 (all-zero vector) -> division by zero -> inf/nan,
         SILENTLY. What do you return instead, and why is that defensible?
       Efficiency observation (notice it, don't obsess):
       - all three sums walk the same indices -> one loop can do all three.
       HAND-CHECK ANCHOR (do this arithmetic on paper first):
       - a={1,2,3}, b={4,5,6}: dot=32, |a|=sqrt(14), |b|=sqrt(77)
         -> expect ~0.9746. Your function MUST print this.
       ------------------------------------------------------------------ */
    float cosine_similarity(const std::vector<float>& a,
                            const std::vector<float>& b) const;

    std::vector<DocumentChunk> storage;
    int expected_dim_ = 384;        // all-MiniLM-L6-v2 (ingestion's model)
};
