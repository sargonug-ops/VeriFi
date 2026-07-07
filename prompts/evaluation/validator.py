def validate_response(response: dict) -> dict:
    """
    Basic QA checks for VeriFi responses.

    Checks whether the answer has the expected structure and whether
    source citations match the project's frontend/API schema.
    """
    answer = response.get("answer", "")
    sources = response.get("sources", [])

    checks = {
        "has_answer": bool(answer.strip()),
        "has_sources": len(sources) > 0,
        "sources_have_text": all("text" in source for source in sources),
        "sources_have_source_document": all("source_document" in source for source in sources),
        "sources_have_page_number": all("page_number" in source for source in sources),
        "sources_have_score": all("score" in source for source in sources),
        "answer_not_empty_guess": bool(answer.strip()),
    }

    checks["passed"] = all(checks.values())
    return checks