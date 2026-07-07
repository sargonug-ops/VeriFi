import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import type { SourceCitation } from "../api/types";
import { AssistantMessage } from "../components/chat/AssistantMessage";
import { ChatInput } from "../components/chat/ChatInput";
import { UserMessage } from "../components/chat/UserMessage";
import { LeftSidebar } from "../components/layout/LeftSidebar";
import { RightPanel } from "../components/layout/RightPanel";
import { type ChatMessage, useChat } from "../hooks/useChat";

const INTRO_MESSAGE: ChatMessage = {
  role: "assistant",
  content:
    "Ask a Fidelity-style financial policy question. I will simulate embedding your query, searching a custom C++ vector database, retrieving policy chunks, and generating a grounded response with citations.",
  sources: [],
};

function MessageList({ messages }: { messages: ChatMessage[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message, index) =>
        message.role === "user" ? (
          <UserMessage key={index} content={message.content} />
        ) : (
          <AssistantMessage
            key={index}
            content={message.content}
            sources={message.sources}
          />
        ),
      )}
      <div ref={bottomRef} />
    </div>
  );
}

export default function ChatPage() {
  const [searchParams] = useSearchParams();
  const [messages, setMessages] = useState<ChatMessage[]>([INTRO_MESSAGE]);
  const [draft, setDraft] = useState("");
  const [activeQuestion, setActiveQuestion] = useState<string | null>(null);
  const { sendMessage, isLoading, error, resetError } = useChat();
  const initialQuestionSent = useRef(false);

  const lastSources: SourceCitation[] =
    (
      messages
        .filter((m) => m.role === "assistant")
        .at(-1) as Extract<ChatMessage, { role: "assistant" }>
    )?.sources ?? [];

  function handleSend(message: string) {
    resetError();
    setActiveQuestion(message);
    sendMessage(message, setMessages, messages);
    setDraft("");
  }

  // Auto-send question passed from landing page via ?q=
  useEffect(() => {
    const q = searchParams.get("q");
    if (q && !initialQuestionSent.current) {
      initialQuestionSent.current = true;
      handleSend(q);
    }
  }, []);

  return (
    <div className="app-layout">
      <LeftSidebar
        onSelectQuestion={handleSend}
        activeQuestion={activeQuestion}
        isLoading={isLoading}
      />

      <div className="chat-area">
        <header className="chat-header">
          <div>
            <p className="chat-header__eyebrow">Fidelity-Style RAG Chatbot</p>
            <h1 className="chat-header__title">Financial Policy Assistant</h1>
          </div>
          <div className="demo-mode-badge">
            <span className="demo-mode-badge__dot" />
            Demo mode
          </div>
        </header>

        <div className="chat-messages">
          <MessageList messages={messages} />

          {isLoading && (
            <div className="message message--assistant">
              <span className="message__avatar message__avatar--fa">FA</span>
              <div className="message__bubble message__bubble--assistant">
                <p className="typing-indicator">
                  <span />
                  <span />
                  <span />
                </p>
              </div>
            </div>
          )}

          {error && (
            <div className="error-banner" role="alert">
              <p>
                {error instanceof Error
                  ? error.message
                  : "Something went wrong. Please try again."}
              </p>
              <button type="button" onClick={resetError}>
                Dismiss
              </button>
            </div>
          )}
        </div>

        <ChatInput
          onSubmit={handleSend}
          disabled={isLoading}
          value={draft}
          onValueChange={setDraft}
        />
      </div>

      <RightPanel sources={lastSources} />
    </div>
  );
}
