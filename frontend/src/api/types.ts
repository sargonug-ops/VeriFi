/** Matches the C++ DocumentChunk struct and ingestion JSONL output. */
export interface DocumentChunk {
  chunk_index: number;
  text: string;
  source_document: string;
  page_number: number;
  embedding: number[];
}

/** FastAPI backend source shape (backend/src/main.py). */
export interface BackendSource {
  doc: string;
  page: number;
  snippet: string;
  score: number;
}

/** FastAPI POST /chat request body. */
export interface BackendChatRequest {
  query: string;
}

/** FastAPI POST /chat response body. */
export interface BackendChatResponse {
  answer: string;
  sources: BackendSource[];
}

/** Normalized source citation used throughout the UI. */
export interface SourceCitation {
  text: string;
  source_document: string;
  page_number: number;
  score: number;
  title?: string;
  section?: string;
}

export interface ChatRequest {
  query: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceCitation[];
}

export interface HealthResponse {
  status: "ok" | "degraded";
}
