#pragma once
#include <string>
#include <vector>



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

struct SearchResult {
    float score;                    // cosine similarity, roughly [-1, 1]
    std::string text;
    std::string source_document;
    int page_number;
};
