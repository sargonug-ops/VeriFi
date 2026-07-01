/** Matches the C++ DocumentChunk struct and ingestion JSONL output. */
export interface DocumentChunk {
  text: string;
  source_document: string;
  page_number: number;
  embedding: number[];
}

/** Source citation returned by POST /chat (chunk metadata + relevance, no embedding). */
export interface SourceCitation {
  text: string;
  source_document: string;
  page_number: number;
  score: number;
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceCitation[];
}

export interface HealthResponse {
  status: "ok" | "degraded";
}
