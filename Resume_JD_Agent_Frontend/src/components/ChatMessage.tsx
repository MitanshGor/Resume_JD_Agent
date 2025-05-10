
import { Message } from "@/hooks/useChat";
import { cn } from "@/lib/utils";
import { User, FileText } from "lucide-react";
import Markdown from 'react-markdown';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={cn(
        "py-2 flex w-full items-start gap-2",
        message.role === 'user' && "justify-end"
      )}
    >
      {message.role === 'assistant' && (
        <div className="w-8 h-8 rounded-full bg-chat-assistant/20 flex items-center justify-center flex-shrink-0">
          <FileText className="h-4 w-4 text-chat-assistant" />
        </div>
      )}

      <div
        className={cn(
          "max-w-[85%]",
          message.role === 'user' && "user-message",
          message.role === 'assistant' && "assistant-message",
          message.role === 'system' && "system-message"
        )}
      >
        {message.role === 'assistant' ? (
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <Markdown>{message.content}</Markdown>
          </div>
        ) : (
          <div className="whitespace-pre-wrap">{message.content}</div>
        )}
        <div className="text-xs text-muted-foreground mt-1 text-right">
          {formatTime(message.timestamp)}
        </div>
      </div>

      {message.role === 'user' && (
        <div className="w-8 h-8 rounded-full bg-chat-user/20 flex items-center justify-center flex-shrink-0">
          <User className="h-4 w-4 text-chat-user" />
        </div>
      )}
    </div>
  );
}
