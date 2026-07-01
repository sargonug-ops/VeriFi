import type { SourceCitation } from "../../api/types";
import { SourceList } from "../citations/SourceList";

interface AssistantMessageProps {
  content: string;
  sources: SourceCitation[];
}

export function AssistantMessage({ content, sources }: AssistantMessageProps) {
  return (
    <div className="message message--assistant">
      <p className="message__content">{content}</p>
      <SourceList sources={sources} />
    </div>
  );
}
