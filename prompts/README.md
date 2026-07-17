# Prompt Engineering, Integration and QA

Author: Divya Machiraju  
Role: Prompting + QA  

## Purpose

This folder contains VeriFi's prompt engineering and QA materials for the RAG pipeline.

It supports:
- Sprint 1–2: RAG prompt design, citation requirements, and QA planning
- Sprint 3 (User Story 3.4): chunk integration, LLM response generation, and automated QA validation

## Sprint 1 & 2 Files

- `system_prompt.txt`  
  Main system prompt that tells the AI to answer only from retrieved documents.

- `prompt_template.txt`  
  Template for combining the user question, retrieved chunks, and system prompt.

- `prompt_builder.py`  
  Builds the final prompt sent to the LLM from the user question and retrieved chunks.

- `prompt_versions/prompt_v1.txt`  
  First saved version of the prompt.

- `evaluation/qa_checklist.md`  
  Manual checklist for judging response quality.

- `evaluation/test_questions.json`  
  Test questions for common financial policy cases and edge cases.

- `evaluation/expected_outputs.md`  
  Examples of passing, insufficient-context, and prompt-injection-safe outputs.

- `evaluation/validator.py`  
  Response-format validator for checking answers and citations.

## Sprint 3 (User Story 3.4)

- `chunk_adapter.py`  
  Normalizes retrieved chunks from ingestion, vector store, or legacy API formats into one canonical shape.

- `llm_client.py`  
  Calls the LLM API, or returns a mock response for local testing.

- `rag_pipeline.py`  
  Main entry point. Exposes `generate_rag_response()` for the backend to call.

- `evaluation/run_qa_tests.py`  
  Automated QA test runner using `test_questions.json`.

- `evaluation/test_results_sprint3.md`  
  Saved Sprint 3 QA test results for the sprint report.

- `INTEGRATION.md`  
  Backend handoff instructions for wiring this module into `POST /chat`.

- `requirements.txt`  
  Python dependencies for LLM integration (`openai`).

## Canonical Chunk / Source Format

All prompt and QA code uses these field names:

- `text`
- `source_document`
- `page_number`
- `score`

Legacy backend mock fields (`doc`, `page`, `snippet`) are supported through `chunk_adapter.py`.

## Run QA Tests

From the `prompts` folder:

```bash
cd prompts
export VERIFI_USE_MOCK_LLM=true
python3 evaluation/run_qa_tests.py

```

Expected result: `10/10 passed`

### Optional: run with a real LLM

```bash
cd prompts
pip3 install -r requirements.txt
export OPENAI_API_KEY=your-real-key-here
export VERIFI_USE_MOCK_LLM=false
python3 evaluation/run_qa_tests.py
```

## Backend Integration

Ethan should import and call:

```python
from rag_pipeline import generate_rag_response

return generate_rag_response(request.query, retrieved_chunks)
```

See `INTEGRATION.md` for full wiring instructions.

## QA Focus

A VeriFi response should pass QA only if it:
1. Uses retrieved document chunks.
2. Avoids unsupported claims.
3. Includes citations when sources are available.
4. Handles missing information honestly.
5. Ignores prompt-injection attempts.