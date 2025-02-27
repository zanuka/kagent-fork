import { messageUtils } from "@/lib/utils";
import ToolCallDisplay from "./ToolCallDisplay";
import LLMCallModal from "./LLMCallModal";
import { TruncatableText } from "./TruncatableText";
import { Message, Run } from "@/types/datamodel";
import { Bot } from "lucide-react";

interface ChatMessageProps {
  message: Message;
  run: Run | null;
  isStreaming?: boolean;
}

export default function ChatMessage({ message, run, isStreaming = false }: ChatMessageProps) {
  if (!message || !message.config) {
    return null;
  }

  const messageObject = message.config;
  const messageContent = messageObject.content;
  const source = message.config.source;
  const isUser = source === "user";

  if (source === "system" || source === "kagent_user") {
    return null;
  }

  if (isUser) {
    return (
      <div className="flex items-center gap-2 text-sm text-white/50 border-l-blue-500 bg-neutral-800 border border-[#3A3A3A] border-l-2 py-2 px-4">
        <div className="flex flex-col gap-1 w-full">
          <div className="text-xs font-bold text-white/80">User</div>
          <TruncatableText content={String(messageContent)} isStreaming={false} className="break-all" />
        </div>
      </div>
    );
  }

  if (!isStreaming) {
    if (messageUtils.isTeamResult(messageObject)) {
      return (
        <div className="text-sm text-white/80 bg-neutral-800 border border-white/50 p-4">
          <span className="font-semibold">Task completed</span>
          <ul className="mt-2 text-white/60">
            <li>Duration: {Math.floor(messageObject.duration)} seconds </li>
            <li>Messages sent: {messageObject.task_result.messages.length}</li>
          </ul>
        </div>
      );
    }

    if (messageUtils.isFunctionExecutionResult(messageContent) || (messageUtils.isToolCallContent(messageContent) && run)) {
      return <ToolCallDisplay currentMessage={message} currentRun={run} />;
    }

    if (messageUtils.isLlmCallEvent(messageContent)) {
      return <LLMCallModal content={String(messageContent)} />;
    }
  }

  return (
    <>
      <div className="flex items-center gap-2 text-sm text-white/50 border-l-violet-500 bg-transparent border-l-2 py-2 px-4">
        <div className="flex flex-col gap-1 w-full">
          <div className="text-xs font-bold text-white/80">{source}</div>
          <TruncatableText content={String(messageContent)} isStreaming={isStreaming} className="break-all" />
        </div>
      </div>
    
    </>
  );
}
