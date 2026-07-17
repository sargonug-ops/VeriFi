import { delay, http, HttpResponse } from "msw";
import { toBackendChatResponse } from "../api/normalize";
import type { HealthResponse } from "../api/types";
import { getMockResponse } from "./data";

// Match absolute or relative /api paths from any page (/, /chat, /chat?q=...).
export const handlers = [
  http.get("*/api/health", () => {
    return HttpResponse.json<HealthResponse>({ status: "ok" });
  }),

  http.post("*/api/chat", async ({ request }) => {
    const body = (await request.json()) as { query?: string };
    const query = body.query ?? "";

    await delay(600);

    return HttpResponse.json(toBackendChatResponse(getMockResponse(query)));
  }),
];
