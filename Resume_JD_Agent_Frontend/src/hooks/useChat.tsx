
import { useState } from 'react';
import { toast } from 'sonner';

export interface StringKeyValue {
  [key: string]: string;
}
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface AnalysisResult {
  Score: Record<string, number>;
  improvement_tips: string[];
  strengths: string[];
  overall_score: number;
}

const API_URL = 'http://127.0.0.1:5000/analyze'; // Flask backend URL

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'system',
      content: 'Welcome to Job Application AI Assistant! Enter your resume and a job description to get personalized insights on how well your resume aligns with the job requirements.',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content,
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const hasResume = checkIfContainsResume(content);
      const hasJobDescription = checkIfContainsJobDescription(content);

      // Check if both resume and job description are provided
      if (!hasResume || !hasJobDescription) {
        const missingMsg = !hasResume && !hasJobDescription 
          ? "Both your resume and job description are required for analysis."
          : !hasResume 
            ? "Please provide your resume for analysis."
            : "Please provide the job description for analysis.";
        
        const systemMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'system',
          content: missingMsg,
          timestamp: new Date(),
        };
        
        setMessages((prev) => [...prev, systemMessage]);
        setIsLoading(false);
        return;
      }

      // In development, we can use the mock API response
      if (process.env.NODE_ENV === 'development' && !API_URL.startsWith('http')) {
        // Mock data for development
        await new Promise((resolve) => setTimeout(resolve, 2000));
        const mockApiResponse = getMockAnalysisResponse();
        const formattedResponse = formatAnalysisResponse(mockApiResponse);
        
        const assistantMessage: Message = {
          id: (Date.now() + 2).toString(),
          role: 'assistant',
          content: formattedResponse,
          timestamp: new Date(),
        };
        
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        // In production, make a real API call to the Flask backend
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' ,
            'Accept': 'application/json',
          },
          body: JSON.stringify({
              "session_id": "test-session-001",
               "message": content })
        });
        
        if (!response.ok) {
          throw new Error('Failed to get analysis from server');
        }

        const data = await response.json();
        // console.log('Typeof API Response:', typeof data);
        // console.log('API Response:', data);
        // string to json
       let temp = data.slice(7, -3);
       temp = temp.trim();
        console.log('API Response:', temp);
       temp  = JSON.parse(temp);
        console.log('Typeof API Response 123 :', typeof temp);
        let  formattedResponse = '';
        if(typeof temp === 'string') {
          formattedResponse = data
        } else {
          formattedResponse = formatAnalysisResponse(temp);
        }

        console.log('API Response 2:', data);
        // console.log('Formatted Response:', formattedResponse);
        
        const assistantMessage: Message = {
          id: (Date.now() + 2).toString(),
          role: 'assistant',
          content: formattedResponse,
          timestamp: new Date(),
        };
        

        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to get a response. Please try again.');
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: 'Sorry, I encountered an error processing your request. Make sure the Flask backend is running.',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const checkIfContainsResume = (content: string) => {
    // In a real application, this would use NLP or pattern matching
    // For this demo, we'll just check for keywords
    if (content.toLowerCase().includes('resume') || 
        content.toLowerCase().includes('cv') ||
        content.toLowerCase().includes('work experience') ||
        content.toLowerCase().includes('skills')) {
      return true;
    }
    
    return false;
  };

  const checkIfContainsJobDescription = (content: string) => {
    // In a real application, this would use NLP or pattern matching
    if (content.toLowerCase().includes('job description') || 
        content.toLowerCase().includes('job post') ||
        content.toLowerCase().includes('job requirement') ||
        content.toLowerCase().includes('position')) {
      return true;
    }
    
    return false;
  };

  const getMockAnalysisResponse = (): AnalysisResult | StringKeyValue => {
    // This simulates the JSON response from the Flask API
    return {
      Score: {
        "Technical Skills Match": 78,
        "Experience Relevance": 82,
        "Education Alignment": 90,
        "Keyword Optimization": 65,
        "Cultural Fit": 73
      },
      improvement_tips: [
        "Add more industry-specific keywords from the job description",
        "Quantify your achievements with metrics and numbers",
        "Highlight specific projects relevant to this role",
        "Include certifications mentioned in the job requirements",
        "Customize your skills section to better match the job needs"
      ],
      strengths: [
        "Strong educational background that aligns with the role",
        "Relevant experience in the industry",
        "Good demonstration of technical skills",
        "Clear communication style in resume",
        "Appropriate resume length and organization"
      ],
      overall_score: 76
    };
  };

  

const formatAnalysisResponse = (result: AnalysisResult | StringKeyValue): string => {
  let response = `## Resume Analysis Results\n\n`;
  if (typeof result === 'string') {
    return result;
  }
  // Add overall score with emoji indicator
  let scoreEmoji = "🟢";
  if (Number(result.overall_score) < 60) scoreEmoji = "🔴";
  else if (Number(result.overall_score) < 80) scoreEmoji = "🟡";

  response += `### Overall Match Score: ${scoreEmoji} ${result.overall_score}\n`;
  response += `*Your resume's alignment with this job position*\n\n`;

  // Add category scores
  response += `### Detailed Scores\n`;
  Object.entries(result.Score).forEach(([category, score]) => {
    let categoryEmoji = "✅";
    if (score < 60) categoryEmoji = "❌";
    else if (score < 80) categoryEmoji = "⚠️";

    response += `- **${category}**: ${score} ${categoryEmoji}\n`;
  });

  // Add strengths
  response += `\n### Your Strengths\n`;
  if (Array.isArray(result.strengths)) {
    result.strengths.forEach(strength => {
      response += `- ${strength}\n`;
    });
  } else {
    response += `- ${result.strengths}\n`;
  }

  // Add improvement tips
  response += `\n### Improvement Suggestions\n`;
  if (Array.isArray(result.improvement_tips)) {
    result.improvement_tips.forEach(tip => {
      response += `- ${tip}\n`;
    });
  } else {
    response += `- ${result.improvement_tips}\n`;
  }

  // Add conclusion
  // result.overall_score = "85/100"
  // overall_score = Number => 85 
  const overallScore = Number(result.overall_score.toString().slice(0, 2));
  if (overallScore >= 80) {
    response += `\n**✅ Excellent match!** Your resume is well-aligned with this job. Consider applying soon with minor adjustments.`;
  } else if (overallScore >= 60) {
    response += `\n**⚠️ Good potential!** With some targeted improvements, your resume could be a strong match for this position.`;
  } else {
    response += `\n**❌ Needs significant improvements.** Consider developing more relevant skills or reworking your resume to better highlight applicable qualifications.`;
  }

  return response;
};

  const clearChat = () => {
    setMessages([
      {
        id: Date.now().toString(),
        role: 'system',
        content: 'Chat has been cleared. Enter your resume and a job description to get personalized insights on how well your resume aligns with the job requirements.',
        timestamp: new Date(),
      },
    ]);
  };

  return {
    messages,
    sendMessage,
    clearChat,
    isLoading,
  };
}
