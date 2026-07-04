def validate_response(response: dict) -> dict:
    """
    Basic QA checks for VeriFi responses.

    This does not prove the answer is perfect, but it checks whether
    the response follows the expected structure for Sprint 2 QA.
    """
    answer = response.get("answer", "")
    sources = response.get("sources", [])

    checks = {
        "has_answer": bool(answer.strip()),
        "has_sources": len(sources) > 0,
        "sources_have_doc": all("doc" in source for source in sources),
        "sources_have_page": all("page" in source for source in sources),
        "sources_have_snippet": all("snippet" in source for source in sources),
        "avoids_empty_guessing": "I don't know" not in answer.lower(),
    }

    checks["passed"] = all(checks.values())
    return checks