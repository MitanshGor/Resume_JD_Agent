
import { useEffect, useRef } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ThemeToggle } from "./ThemeToggle";
import { useChat } from "@/hooks/useChat";
import { Button } from "@/components/ui/button";

export function ChatInterface() {
  const { messages, sendMessage, clearChat, isLoading } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-accent/30 to-background">
      <div className="flex items-center justify-between p-4 border-b bg-background/75 backdrop-blur-sm sticky top-0 z-10">
        <h1 className="text-lg font-semibold bg-gradient-to-r from-primary to-chat-assistant bg-clip-text text-transparent">
          Job Application AI Assistant
        </h1>
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            onClick={clearChat}
            size="sm"
            className="text-sm"
          >
            Clear Chat
          </Button>
          <ThemeToggle />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
        
        {isLoading && (
          <div className="flex justify-center items-center py-2">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
              <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
              <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
            </div>
          </div>
        )}
      </div>

      <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
    </div>
  );
}
