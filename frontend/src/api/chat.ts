import { normalizeChatResponse } from "./normalize";
import { apiFetch } from "./client";
import type {
  BackendChatResponse,
  ChatRequest,
  ChatResponse,
  HealthResponse,
} from "./types";

export function getHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/health");
}

export function postChat(request: ChatRequest): Promise<ChatResponse> {
  return apiFetch<BackendChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({ query: request.query }),
  }).then(normalizeChatResponse);
}
