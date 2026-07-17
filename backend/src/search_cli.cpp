// API bridge adapter — calls Chris's VectorStore public API.
// Does not modify VectorStore.cpp; links it at build time.
//
// Usage:
//   search_cli <path-to-chunks.jsonl>
//   echo '{"embedding":[...],"top_k":5}' | search_cli output/chunks.jsonl
//
// Exit codes: 0 success, 1 load failure, 2 bad input

#include "VectorStore.h"
#include <json.hpp>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using json = nlohmann::json;

static json search_result_to_json(const SearchResult& result) {
    return json{
        {"score", result.score},
        {"text", result.text},
        {"source_document", result.source_document},
        {"page_number", result.page_number},
    };
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "usage: search_cli <chunks.jsonl>\n";
        return 2;
    }

    const std::string chunks_path = argv[1];
    VectorStore store;

    if (!store.load_from_jsonl(chunks_path)) {
        std::cerr << "failed to load: " << chunks_path << "\n";
        return 1;
    }

    std::ostringstream input_buffer;
    input_buffer << std::cin.rdbuf();
    const std::string input = input_buffer.str();

    if (input.empty()) {
        std::cerr << "expected JSON on stdin: {\"embedding\":[...],\"top_k\":5}\n";
        return 2;
    }

    json request;
    try {
        request = json::parse(input);
    } catch (const json::parse_error& e) {
        std::cerr << "invalid JSON: " << e.what() << "\n";
        return 2;
    }

    if (!request.contains("embedding") || !request["embedding"].is_array()) {
        std::cerr << "missing or invalid 'embedding' array\n";
        return 2;
    }

    std::vector<float> embedding;
    try {
        embedding = request["embedding"].get<std::vector<float>>();
    } catch (const json::type_error& e) {
        std::cerr << "embedding must be array of numbers: " << e.what() << "\n";
        return 2;
    }

    int top_k = 5;
    if (request.contains("top_k")) {
        if (!request["top_k"].is_number_integer()) {
            std::cerr << "'top_k' must be an integer\n";
            return 2;
        }
        top_k = request["top_k"].get<int>();
    }

    const std::vector<SearchResult> results = store.search(embedding, top_k);

    json output = json::array();
    for (const SearchResult& result : results) {
        output.push_back(search_result_to_json(result));
    }

    std::cout << output.dump() << "\n";
    return 0;
}
