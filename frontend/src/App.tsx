import { useState } from "react";
import { ChatInput } from "./components/chat/ChatInput";
import { EmptyState } from "./components/chat/EmptyState";
import { MessageList } from "./components/chat/MessageList";
import { AppShell } from "./components/layout/AppShell";
import { ConnectionStatus } from "./components/layout/ConnectionStatus";
import { type ChatMessage, useChat } from "./hooks/useChat";

function ErrorBanner({
  message,
  onDismiss,
}: {
  message: string;
  onDismiss: () => void;
}) {
  return (
    <div className="error-banner" role="alert">
      <p>{message}</p>
      <button type="button" onClick={onDismiss}>
        Dismiss
      </button>
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const { sendMessage, isLoading, error, resetError } = useChat();

  function handleSend(message: string) {
    resetError();
    sendMessage(message, setMessages, messages);
  }

  return (
    <AppShell>
      <div className="chat-panel">
        <div className="chat-panel__status">
          <ConnectionStatus />
        </div>

        {error && (
          <ErrorBanner
            message={
              error instanceof Error
                ? error.message
                : "Something went wrong. Please try again."
            }
            onDismiss={resetError}
          />
        )}

        <div className="chat-panel__messages">
          {messages.length === 0 ? (
            <EmptyState
              onSelectQuestion={(question) => {
                setDraft(question);
                handleSend(question);
              }}
              disabled={isLoading}
            />
          ) : (
            <MessageList messages={messages} />
          )}

          {isLoading && (
            <p className="loading-indicator" aria-live="polite">
              Retrieving sources and generating answer…
            </p>
          )}
        </div>

        <ChatInput
          onSubmit={handleSend}
          disabled={isLoading}
          value={draft}
          onValueChange={setDraft}
        />
      </div>
    </AppShell>
  );
}
