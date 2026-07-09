import { delay, http, HttpResponse } from "msw";
import { toBackendChatResponse } from "../api/normalize";
import type { HealthResponse } from "../api/types";
import { getMockResponse } from "./data";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

export const handlers = [
  http.get(`${API_BASE_URL}/health`, () => {
    return HttpResponse.json<HealthResponse>({ status: "ok" });
  }),

  http.post(`${API_BASE_URL}/chat`, async ({ request }) => {
    const body = (await request.json()) as { query?: string };
    const query = body.query ?? "";

    await delay(800);

    return HttpResponse.json(toBackendChatResponse(getMockResponse(query)));
  }),
];
