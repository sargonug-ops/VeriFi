#include "VectorStore.h"
#include <fstream>      // std::ifstream
#include <cmath>        // std::sqrt
#include <algorithm>    // std::sort, std::min
// TODO(you): #include the vendored nlohmann header. THINK: given your
// compile command uses -Ilib, what exactly goes between the quotes/brackets?


bool VectorStore::load_from_jsonl(const std::string& filepath) {
    // SHAPE OF THE SOLUTION (order of operations, not code):
    //   open -> check opened -> per-line loop -> skip blanks -> parse ->
    //   extract 5 fields -> validate dim -> build chunk -> push -> true
    //
    // THINK ABOUT while writing:
    // - What does `if (!file)` actually test? -> "ifstream operator bool"
    // - getline's return value IS the loop condition. Why does that idiom
    //   terminate correctly at EOF?
    // - Where does your dimension check go so a bad line can't enter
    //   storage? What do you PRINT when you skip one (a count at the end
    //   beats spam per line)?
    //
    // WHEN STUCK, look up (in this order):
    //   "read file line by line c++ getline"
    //   "nlohmann json parse string example"
    //   "nlohmann json get vector"
    return false; // TODO(you)
}

std::vector<SearchResult> VectorStore::search(
        const std::vector<float>& query_embedding, int top_k) const {
            
            if (query_embedding.empty()) return {};
            if (query_embedding.size() != static_cast<std::size_t>(expected_dim_)) return {};
            if (top_k <= 0) return {};
            if (storage.empty()) return {};

            //Storing the {score, index} pair inside a fector - naming it score_pair
            std::vector<std::pair<float, std::size_t>> score_pair;
            //reserving up to storage.size() in space
            score_pair.reserve(storage.size());

            for(std::size_t index = 0; index < storage.size(); ++index){ 
                //check if embedding empty, skip if true - skip if chunk not the same size as dim expected
                if (storage[index].embedding.empty()) continue;
                if (storage[index].embedding.size() != expected_dim_) continue;
                
                float score = cosine_similarity(query_embedding, static_cast<std::size_t>storage[x].embedding);
                score_pair.push_back(std::make_pair(score, index));
            
            }

            //lambda function for sorting by descending - sort<> defaults to ascends
            std::sort(score_pair.begin(), score_pair.end(), 
            [](const std::pair<float, std::size_t>& a, const std::pair<float, std::size_t>& b)
            {return a.first > b.first});

            if(!(score_pair[0].first > score_pair[1].first)){
                std::printf("error in sorting...\nscore_pair[0] = %f !> score_pair[1] = %f\n", score_pair[0].first, score_pair[1]);
            }



    //   chunk -> sort DESCENDING by score -> take first min(top_k, N) ->
    //   package SearchResults -> return
    //

    return {};
}

//Get total chunks 
std::size_t VectorStore::fetchSize() const {
    return storage.size();
}

//Get width of embedding
int VectorStore::dimension() const {
    if (storage.empty()) return 0;
    return static_cast<int>storage[0].embedding.size();
}

float VectorStore::magnitude(const std::vector<float>& vec) const {

    if (vec.empty()) return 0.0f;
    
    float squareSum {0.0f};

    for (std::size_t i {0}; i < vec.size(); i++) {
        squareSum += vec[i] * vec[i];
    } 

    return std::sqrt(squareSum);
}

    float const VectorStore::dotProduct(const std::vector<float>& vec1, const std::vector<float>& vec2){

        if (vec1.empty() || vec2.empty()) return 0.0f;
        //Update to disclude this chunk in order to avoid polluting data 
        if (vec1.size() != vec2.size()) return 0.0f;

        float dotProductSum {0};

        for (int i {0}; i < vec1.size(); i++) {
            dotProductSum += (vec1[i] * vec2[i]);
        }

        return dotProductSum;
    }


//Each vector has 384 dimensions
//We are generating a single float value PER query, -1 - 1 ranking  
// this value will be used to rank chunks, the higher the score the closer the chunk is to matching the user query 

float VectorStore::cosine_similarity(const std::vector<float>& queryFloat, const std::vector<float>& dataBaseFloat) const {

    const float queryMag = magnitude(queryFloat);
    const float dbMag = magnitude(dataBaseFloat);

    //return empty float
    if (queryMag == 0.0f || dbMag == 0.0f) return 0.0f;
    
    return dotProduct(queryFloat, dataBaseFloat) / (queryMag * dbMag); 
}
