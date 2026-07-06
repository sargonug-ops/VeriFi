"""
VeriFi Backend - FastAPI server
User Story 1.4: /chat endpoint with mocked data + /health check

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="VeriFi API",
    description="Backend API for VeriFi - a RAG-based financial policy chatbot.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# Task 4: CORS - allow the React dev server (localhost:3000) to call this API
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schemas (this doubles as the source of truth for the API contract doc)
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's natural language question.")

    class Config:
        json_schema_extra = {
            "example": {"query": "What is the company's remote work policy?"}
        }


class Source(BaseModel):
    doc: str = Field(..., description="Name/title of the source document.")
    page: int = Field(..., description="Page number the snippet was pulled from.")
    snippet: str = Field(..., description="Short excerpt supporting the answer.")
    score: float = Field(..., description="Relevance score, 0.0-1.0.")


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Employees may work remotely up to 3 days per week, "
                "subject to manager approval.",
                "sources": [
                    {
                        "doc": "Employee_Handbook_2025.pdf",
                        "page": 12,
                        "snippet": "Remote work is permitted up to three (3) days "
                        "per week with manager sign-off.",
                        "score": 0.91,
                    }
                ],
            }
        }


class HealthResponse(BaseModel):
    status: str


# ---------------------------------------------------------------------------
# Task 2: GET /health
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Task 3: POST /chat (hardcoded mock response - no real pipeline yet)
# ---------------------------------------------------------------------------


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest):
    # NOTE: This is intentionally hardcoded per User Story 1.4 scope.
    # Task 1.4 only requires a stable contract for the frontend to build
    # against - real retrieval/LLM integration comes in a later story.
    return {
        "answer": f"This is a mocked response to your question: \"{request.query}\". "
        "Once the retrieval pipeline is connected, this will contain a "
        "real answer grounded in company documents.",
        "sources": [
            {
                "doc": "Employee_Handbook_2025.pdf",
                "page": 12,
                "snippet": "Remote work is permitted up to three (3) days per "
                "week with manager sign-off.",
                "score": 0.91,
            },
            {
                "doc": "Expense_Policy_v2.pdf",
                "page": 4,
                "snippet": "All reimbursement requests must be submitted within "
                "30 days of the expense date.",
                "score": 0.77,
            },
        ],
    }