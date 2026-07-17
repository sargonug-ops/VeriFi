INSUFFICIENT_PHRASES = (
    "could not find enough information",
    "do not provide enough information",
    "no supporting source",
)


def validate_response(response: dict, category: str | None = None) -> dict:
    answer = response.get("answer", "")
    sources = response.get("sources", [])

    checks = {
        "has_answer": bool(answer.strip()),
        "sources_have_text": all("text" in s for s in sources) if sources else True,
        "sources_have_source_document": all("source_document" in s for s in sources) if sources else True,
        "sources_have_page_number": all("page_number" in s for s in sources) if sources else True,
        "sources_have_score": all("score" in s for s in sources) if sources else True,
    }

    if category == "empty_question":
        checks["rejects_empty_input"] = "valid question" in answer.lower()
    elif category == "insufficient_context":
        checks["admits_insufficient_info"] = any(p in answer.lower() for p in INSUFFICIENT_PHRASES)
    elif category in ("basic_policy_question", "fees", "transfers", "beneficiaries", "multi_source_question"):
        checks["has_sources"] = len(sources) > 0
    elif category == "unrelated_question":
        checks["handles_unrelated"] = any(p in answer.lower() for p in INSUFFICIENT_PHRASES)

    checks["passed"] = all(checks.values())
    return checks