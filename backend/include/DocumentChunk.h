#pragma once
#include <string>
#include <vector>

/* ============================================================================
   STUDY BANK — this file
   ----------------------------------------------------------------------------
   Concepts to understand before/while reading this file:
   1. "#pragma once" vs classic include guards (#ifndef/#define/#endif)
      -> look up: "pragma once vs include guards" — know what problem BOTH
         solve (the same header pasted twice into one translation unit).
   2. What a "translation unit" is — one .cpp + everything it #includes.
      This is the concept that explains every linker error you'll ever get.
   3. struct vs class in C++ — the ONLY difference is default access.
      Why is struct the idiomatic choice for plain data bundles like these?
   4. Why these structs live in a header while function BODIES live in .cpp
      -> look up: "C++ header implementation split" / "one definition rule"
   ============================================================================ */

// Mirrors ONE line of ingestion's output/chunks.jsonl exactly:
// {"chunk_index": 0, "text": "...", "source_document": "...",
//  "page_number": 1, "embedding": [ ... 384 floats ... ]}
//
// THINK ABOUT: why must these field names/types track the JSON contract?
// What breaks (and WHERE does it break — compile time or runtime?) if
// ingestion renames a field and you don't?
struct DocumentChunk {
    int chunk_index;
    std::string text;
    std::string source_document;
    int page_number;
    std::vector<float> embedding;   // expected length: 384 (all-MiniLM-L6-v2)
};

// What search() returns to the caller, best match first.
//
// THINK ABOUT: why a separate struct instead of returning DocumentChunk?
// (Hint: the caller needs the score, and doesn't need the raw embedding
//  copied back out. What does copying a 384-float vector per result cost?)
struct SearchResult {
    float score;                    // cosine similarity, roughly [-1, 1]
    std::string text;
    std::string source_document;
    int page_number;
};
