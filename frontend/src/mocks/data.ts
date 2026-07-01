import type { ChatResponse } from "../api/types";

export const MOCK_RESPONSES: Record<string, ChatResponse> = {
  margin: {
    answer:
      "If a margin call is issued, the client must deposit funds within 3 business days. Failure to meet the margin call may result in the broker liquidating positions to cover the deficiency.",
    sources: [
      {
        text: "If a margin call is issued, the client must deposit funds within 3 days.",
        source_document: "Fidelity_Margin_Rules_2026.pdf",
        page_number: 12,
        score: 0.94,
      },
      {
        text: "The firm reserves the right to liquidate securities without prior notice if margin requirements are not satisfied within the prescribed period.",
        source_document: "Fidelity_Margin_Rules_2026.pdf",
        page_number: 14,
        score: 0.81,
      },
    ],
  },
  withdrawal: {
    answer:
      "Withdrawal requests are typically processed within 1–3 business days. Electronic transfers to linked bank accounts may take an additional 1–2 business days to appear.",
    sources: [
      {
        text: "Standard withdrawal requests are processed within one to three business days of receipt.",
        source_document: "terms-and-conditions.pdf",
        page_number: 8,
        score: 0.89,
      },
    ],
  },
  default: {
    answer:
      "Based on the available policy documents, I could not find a specific passage that directly answers your question. Please try rephrasing or ask about margin rules, withdrawals, or account terms.",
    sources: [],
  },
};

export function getMockResponse(message: string): ChatResponse {
  const lower = message.toLowerCase();

  if (lower.includes("margin")) {
    return MOCK_RESPONSES.margin;
  }
  if (lower.includes("withdraw")) {
    return MOCK_RESPONSES.withdrawal;
  }

  return MOCK_RESPONSES.default;
}
