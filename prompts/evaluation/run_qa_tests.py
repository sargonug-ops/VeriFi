import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_pipeline import generate_rag_response
from validator import validate_response

SAMPLE_CHUNKS = [
    {
        "text": "Required minimum distributions generally must begin by April 1 of the year after the account owner turns 73.",
        "source_document": "RMD-GUIDE-2026",
        "page_number": 1,
        "score": 0.92,
    },
    {
        "text": "Online equity and ETF trades may be commission-free; wire transfers and other services may incur fees.",
        "source_document": "FEE-SCH-031",
        "page_number": 3,
        "score": 0.88,
    },
]

def main():
    tests = json.loads((Path(__file__).parent / "test_questions.json").read_text())
    passed = 0
    for t in tests:
        chunks = [] if t["category"] in ("unrelated_question", "insufficient_context") else SAMPLE_CHUNKS
        result = generate_rag_response(t["question"], chunks)
        checks = validate_response(result, t.get("category"))
        status = "PASS" if checks["passed"] else "FAIL"
        if checks["passed"]:
            passed += 1
        print(f"{t['id']} [{t['category']}]: {status} — {checks}")
    print(f"\n{passed}/{len(tests)} passed")

if __name__ == "__main__":
    main()