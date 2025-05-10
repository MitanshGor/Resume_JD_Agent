
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSendMessage, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const autoResize = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  useEffect(() => {
    autoResize();
  }, [message]);

  return (
    <div className="border-t bg-background/80 backdrop-blur-sm sticky bottom-0 w-full">
      <form onSubmit={handleSubmit} className="p-4 flex items-end gap-2">
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your resume and job description here..."
            rows={1}
            className="min-h-[50px] w-full resize-none border rounded-2xl py-3 pr-12 pl-4"
            disabled={isLoading}
          />
        </div>

        <Button
          type="submit"
          size="icon"
          className={`h-10 w-10 rounded-full ${
            message.trim() ? "bg-primary hover:bg-primary/90" : "bg-muted text-muted-foreground"
          } transition-colors`}
          disabled={!message.trim() || isLoading}
        >
          <Send
            className={`h-4 w-4 ${isLoading ? "animate-pulse" : ""}`}
          />
          <span className="sr-only">Send</span>
        </Button>
      </form>
    </div>
  );
}
