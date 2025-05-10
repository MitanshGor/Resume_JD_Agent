
import { ChatInterface } from "@/components/ChatInterface";
import { ThemeProvider } from "@/context/ThemeContext";
import { cn } from "@/lib/utils";

const Index = () => {
  return (
    <ThemeProvider>
      <div className="min-h-screen w-full flex">
        <div className="flex-1 max-w-5xl mx-auto w-full bg-background shadow-xl md:border-x">
          <ChatInterface />
        </div>
        {/* On larger screens, show empty space on the right */}
        <div className="hidden lg:block flex-1 bg-gradient-to-tl from-accent/30 via-background to-background">
          <div className="h-full flex items-center justify-center">
            <div className="w-full max-w-md px-4">
              <div className={cn(
                "text-center py-12 px-6",
                "rounded-2xl shadow-lg border glass-panel",
              )}>
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-chat-assistant flex items-center justify-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="text-white"
                    >
                      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                  </div>
                </div>
                <h2 className="text-2xl font-semibold mb-2">Job Application AI Assistant</h2>
                <p className="text-primary/80 font-medium mb-4">
                  Align your resume with job success
                </p>
                <p className="text-muted-foreground mb-6">
                  Upload your resume and job description to get personalized insights and improve your chances of landing an interview.
                </p>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <p>• Compare your resume to job descriptions</p>
                  <p>• Discover your strengths and weaknesses</p>
                  <p>• Get actionable improvement tips</p>
                  <p>• See your interview potential score</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
};

export default Index;
