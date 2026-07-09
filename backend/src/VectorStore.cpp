#include "VectorStore.h"
#include <fstream>      // std::ifstream
#include <cmath>        // std::sqrt
#include <algorithm>    // std::sort, std::min
// TODO(you): #include the vendored nlohmann header. THINK: given your
// compile command uses -Ilib, what exactly goes between the quotes/brackets?

/* ============================================================================
   STUDY BANK — this file as a whole
   ----------------------------------------------------------------------------
   - Note the `VectorStore::` prefix on every function — why is it required
     here but absent in the header? -> look up: "scope resolution operator"
   - This file NEVER defines main(). Why does that matter for who can link
     against you? (You answered this earlier in the project — recall it.)
   - Suggested implementation ORDER within this file:
       1) cosine_similarity   (pure math, testable in isolation)
       2) size / dimension    (one-liners; unlock the driver's checkpoints)
       3) load_from_jsonl     (needs real chunks.jsonl on disk)
       4) search              (needs 1 and 3 working)
   ============================================================================ */

//using std::size_t = size;


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
            if (query_embedding.empty()) {}

    // SHAPE OF THE SOLUTION:
    //   guards -> build {score,index} pairs (reserve!) -> score every
    //   chunk -> sort DESCENDING by score -> take first min(top_k, N) ->
    //   package SearchResults -> return
    //
    // THINK ABOUT while writing:
    // - Write ALL guards first. An empty return {} is a valid answer to
    //   invalid input — better than a crash inside the loop.
    // - Your comparator decides the sort direction. After sorting, print
    //   the first pair's score in the driver: is it the LARGEST? If not,
    //   your comparator answered the wrong question.
    // - Loop indices: storage[i].embedding is the chunk's vector; i is
    //   what you keep in the pair so you can find the chunk again later.
    //
    // WHEN STUCK, look up:
    //   "std::sort lambda comparator descending"
    //   "std::pair default comparison"
    return {}; // TODO(you)
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
