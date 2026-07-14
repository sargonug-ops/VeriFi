import { useMutation } from "@tanstack/react-query";
import type { Dispatch, SetStateAction } from "react";
import { postChat } from "../api/chat";
import type { SourceCitation } from "../api/types";

export type ChatMessage =
  | { role: "user"; content: string }
  | { role: "assistant"; content: string; sources: SourceCitation[] };

export function useChat() {
  const mutation = useMutation({
    mutationFn: postChat,
  });

  function sendMessage(
    message: string,
    setMessages: Dispatch<SetStateAction<ChatMessage[]>>,
  ) {
    const trimmed = message.trim();
    if (!trimmed || mutation.isPending) return false;

    const userMessage: ChatMessage = { role: "user", content: trimmed };

    // Show the user message immediately so the UI never looks "stuck" if the
    // request fails or is interrupted during a landing-page redirect.
    setMessages((prev) => [...prev, userMessage]);

    mutation.mutate(
      { query: trimmed },
      {
        onSuccess: (response) => {
          const assistantMessage: ChatMessage = {
            role: "assistant",
            content: response.answer,
            sources: response.sources,
          };
          setMessages((prev) => [...prev, assistantMessage]);
        },
      },
    );

    return true;
  }

  return {
    sendMessage,
    isLoading: mutation.isPending,
    error: mutation.error,
    resetError: mutation.reset,
  };
}
