import os

MOCK_ANSWER = (
    "Answer:\nBased on the retrieved documents.\n\n"
    "Explanation:\nThis is a mock response for local QA testing.\n\n"
    "Sources:\n- See retrieved chunks above."
)


def call_llm(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "")
    use_mock = os.getenv("VERIFI_USE_MOCK_LLM", "false").lower() == "true"

    if use_mock or not api_key:
        return MOCK_ANSWER

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install openai: pip install openai") from exc

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("VERIFI_LLM_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""