# Prompt Engineering, Integration and QA

Author: Divya Machiraju  
Role: Prompting + QA  

## Purpose

This folder contains VeriFi's prompt engineering and QA materials.

It supports Sprint 1 and Sprint 2 work for:
- RAG prompt design
- grounded financial-policy responses
- citation requirements
- prompt evaluation
- QA testing

## Files

- `system_prompt.txt`  
  Main system prompt that tells the AI to answer only from retrieved documents.

- `prompt_template.txt`  
  Template for combining the user question, retrieved chunks, and system prompt.

- `prompt_builder.py`  
  Helper file that builds the final prompt programmatically.

- `prompt_versions/prompt_v1.txt`  
  First saved version of the prompt.

- `evaluation/qa_checklist.md`  
  Manual checklist for judging response quality.

- `evaluation/test_questions.json`  
  Test questions for common financial policy cases and edge cases.

- `evaluation/expected_outputs.md`  
  Examples of passing, insufficient-context, and prompt-injection-safe outputs.

- `evaluation/validator.py`  
  Basic response-format validator for checking answers and citations.

## QA Focus

A VeriFi response should pass QA only if it:
1. Uses retrieved document chunks.
2. Avoids unsupported claims.
3. Includes citations.
4. Handles missing information honestly.
5. Ignores prompt-injection attempts.