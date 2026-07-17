import type {
  BackendChatResponse,
  BackendSource,
  ChatResponse,
  SourceCitation,
} from "./types";

export function normalizeSource(source: BackendSource): SourceCitation {
  return {
    text: source.snippet,
    source_document: source.doc,
    page_number: source.page,
    score: source.score,
  };
}

export function normalizeChatResponse(
  response: BackendChatResponse,
): ChatResponse {
  return {
    answer: response.answer,
    sources: response.sources.map(normalizeSource),
  };
}

/** Convert UI-shaped mock data to the FastAPI wire format for MSW. */
export function toBackendChatResponse(response: ChatResponse): BackendChatResponse {
  return {
    answer: response.answer,
    sources: response.sources.map((source) => ({
      doc: source.source_document,
      page: source.page_number,
      snippet: source.text,
      score: source.score,
    })),
  };
}
