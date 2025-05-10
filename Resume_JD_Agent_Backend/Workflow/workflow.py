
from langchain_ollama import OllamaEmbeddings
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition as tc
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
import os
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
import sys 

# Setting the system path so it could view other files within the directory
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tools.utility import tools
from SingleAgent.singleAgent import Agent
from utils.utils import AgentState

load_dotenv()

class workflow:
    def __init__(self):
        self.memory = MemorySaver()
        self.workflow = StateGraph(AgentState)
        self.graph = None

        embeddings = OllamaEmbeddings(
                            model="nomic-embed-text"
                        )
        self.Tools = tools()
        self.singleAgent = Agent()



        self.tools = ToolNode(self.Tools.toolkit())
        self.workflow_init()
        self.clear = self.clear_all_memory
        
    def workflow_init(self):
        self.workflow.add_node("agent", self.singleAgent.run_agent)
        self.workflow.add_node("tools_execution", self.tools)
        self.workflow.set_entry_point("agent")
        self.workflow.add_conditional_edges(
            "agent",
            tc,
            {
                "tools": "tools_execution",
                END: END,

            },
        )
        self.workflow.add_edge("tools_execution", "agent")
        self.graph = self.workflow.compile(checkpointer=self.memory)
        
    def get_graph(self):
        return self.graph
    
    def clear_all_memory(config, graph01):
      """Clears the conversation history."""
      state = graph01.get_state(config)
      if state and "messages" in state.values:
          messages = state.values["messages"]
          for msg in messages:
            try:
              remove_message = RemoveMessage(id=msg.id)
              graph01.update_state(config, {"messages": remove_message})
            except:
              pass


# if __name__ == "__main__":
    

#     g = workflow ()
#     graph = g.get_graph()

#     # Config for tracking session (use a session_id to persist memory if needed)
#     config = RunnableConfig(configurable={"thread_id": "test-session"})

#     print("Type 'exit' or 'quit' to end the session.\n")

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break

#         # Run the LangGraph with current user input
#         response = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

#         # Extract and print last AI response
#         messages = response.get("messages", [])
#         if messages:
#             last_message = messages[-1]
#             print(f"Agent: {last_message.content}\n")
#         else:
#             print("⚠️ No response generated.\n")