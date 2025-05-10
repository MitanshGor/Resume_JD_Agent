
import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/context/ThemeContext";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ThemeToggleProps {
  className?: string;
}

export function ThemeToggle({ className }: ThemeToggleProps) {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className={cn(
        "rounded-full bg-background border-border w-9 h-9 transition-all", 
        className
      )}
    >
      <Sun className={cn(
        "h-4 w-4 transition-all",
        theme === "dark" ? "opacity-0 scale-0" : "opacity-100 scale-100"
      )} />
      <Moon className={cn(
        "absolute h-4 w-4 transition-all",
        theme === "dark" ? "opacity-100 scale-100" : "opacity-0 scale-0"
      )} />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
