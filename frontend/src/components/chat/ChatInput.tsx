import { useState, type FormEvent } from "react";

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled?: boolean;
  value?: string;
  onValueChange?: (value: string) => void;
}

export function ChatInput({
  onSubmit,
  disabled,
  value: controlledValue,
  onValueChange,
}: ChatInputProps) {
  const [internalValue, setInternalValue] = useState("");
  const value = controlledValue ?? internalValue;

  function setValue(next: string) {
    if (onValueChange) {
      onValueChange(next);
    } else {
      setInternalValue(next);
    }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setValue("");
  }

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        className="chat-input__field"
        placeholder="Ask about Fidelity policy documents…"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        disabled={disabled}
        aria-label="Your question"
      />
      <button
        type="submit"
        className="chat-input__submit"
        disabled={disabled || !value.trim()}
      >
        Send
      </button>
    </form>
  );
}
