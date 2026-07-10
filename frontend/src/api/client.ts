function resolveApiBaseUrl(): string {
  const configured = import.meta.env.VITE_API_URL ?? "/api";

  // Keep absolute env values as-is (http://localhost:8000, etc.).
  if (/^https?:\/\//i.test(configured)) {
    return configured.replace(/\/$/, "");
  }

  // Resolve relative paths against the page origin so navigations like
  // / -> /chat?q=... always hit the same API base.
  const origin =
    typeof window !== "undefined" ? window.location.origin : "http://localhost";
  return new URL(configured, origin).toString().replace(/\/$/, "");
}

const API_BASE_URL = resolveApiBaseUrl();

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const body = await response.text().catch(() => "");
    throw new ApiError(
      body || `Request failed with status ${response.status}`,
      response.status,
    );
  }

  return response.json() as Promise<T>;
}
