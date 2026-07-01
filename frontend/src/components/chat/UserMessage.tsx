interface UserMessageProps {
  content: string;
}

export function UserMessage({ content }: UserMessageProps) {
  return (
    <div className="message message--user">
      <p className="message__content">{content}</p>
    </div>
  );
}
