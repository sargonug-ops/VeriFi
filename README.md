# VeriFi

A C++ and React RAG chatbot that grounds answers in verified policy documents

## Problem Statement

Chatbots deployed across company websites often confidently hallucinate information when handling dense policy inquiries that typically require a human agent. This creates a massive regulatory and financial liability for businesses.

Traditional search tools fail to solve this issue because they rely primarily on exact keyword matches, completely missing the true semantic meaning behind a consumer's question. Our application solves this by forcing the AI to base its conversational responses strictly on real, verified company policy documents retrieved dynamically at query time.

## How It Works

We designed VeriFi to run in two phases — one that happens once, ahead of
time, and one that runs on every question.

**Setup (once):** The policy documents are split into small passages
("chunks"), and an embedding model converts each chunk into a vector — a list
of numbers that captures its meaning. Every chunk and its vector are loaded
into the in-memory C++ vector store.

**Per query (every question):**
1. A user asks a question in the React interface.
2. The same embedding model converts that question into a vector.
3. The C++ vector store compares the question vector against every stored
   chunk using cosine similarity and returns the top-K most semantically
   relevant passages.
4. Those passages, the question, and a grounding system prompt are assembled
   into a single request to the LLM.
5. The LLM produces a conversational answer constrained to the retrieved
   passages, and the UI displays it with citations to the source documents.

Because the LLM only ever sees passages actually retrieved from verified
documents, its answers stay anchored to real sources — which reduces
hallucination, though it does not eliminate it.

## Project Goals

1. Build a Custom Vector Database: Implement a ultra-fast semantic vector database from scratch (a lightweight varient of Pinecone) that locates documents based on geometric meaning rather than simple text matching.

2. Implement an End-to-End RAG Pipeline: Seamlessly integrate the C++ search engine into a full-stack Retrieval-Augmented Generation pipeline (similar to LangChain) to reduce AI hallucinations by grounding responses in verified facts.

3. Maintain a Focused Scope: Restrict the dataset to official policy documents available from Fidelity Investments to keep scope tight and demo-able within the development cycle.


## Tech Stack & Divison of Roles

Planned Stack: C++, React, Embedding API / LLM API 

1. Data Ingestion Lead [Srushti]: Sources public PDFs, writes parsing scripts to chunk dense text, and generates the initial vector embeddings.

2. Vector Store Engineer / Project Owner [ChristopherZarraga]: Designs the C++ memory structures, implements the cosine-similarity math, and optimizes the O(N) ranking.

3. API / Backend Bridge [Ethan]: Implements the cpp-httplib C++ server, handles JSON serialization, and manages asynchronous network calls to the embedding and LLM APIs.

4. Frontend React Developer []: Builds the React chat dashboard, handles loading states, and renders the conversational UI with dynamic source citations.

5. Integration, Prompting & QA []: Designs system prompts to keep the LLM grounded in retrieved text, tests edge cases, manages GitHub version control, and prepares the live final demonstration.