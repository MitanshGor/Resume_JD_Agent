import os
import sys
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition as tc
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langchain.tools.base import ToolException
from langgraph.prebuilt import ToolNode

# Set up system path for local imports
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tools.utility import tools
from SingleAgent.singleAgent import Agent
from utils.utils import AgentState

load_dotenv()


# ✅ Custom ToolNode that tracks the last tool used
class ToolNodeWithTracking(ToolNode):
    def invoke(self, input, config=None):
        result = super().invoke(input, config)
        if result and "tool_call" in result:
            input["last_tool"] = result["tool_call"].name
        return input


# ✅ Discord Router to determine which Discord tool to run after a DB tool
def discord_tool_router(state):
    last_tool = state.get("last_tool")
    if last_tool == "insert_candidate":
        return "discord_user_create"
    elif last_tool == "update_candidate":
        return "discord_user_update"
    elif last_tool == "delete_candidate":
        return "discord_user_delete"
    return "__end__"



class workflow:
    def __init__(self):
        self.memory = MemorySaver()
        self.workflow = StateGraph(AgentState)
        self.graph = None

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.Tools = tools()
        self.singleAgent = Agent()

        # Register tools and enhanced ToolNode
        self.tools = ToolNodeWithTracking(self.Tools.toolkit())

        self.workflow_init()

        self.clear = self.clear_all_memory

    def workflow_init(self):
        self.workflow.add_node("agent", self.singleAgent.run_agent)
        self.workflow.add_node("tools_execution", self.tools)

        discord_tool_map = {
            tool.name: tool for tool in self.Tools.toolkit()
            if tool.name.startswith("discord_user_")
        }
        self.workflow.add_node("discord_user_create", discord_tool_map["discord_user_create"])
        self.workflow.add_node("discord_user_update", discord_tool_map["discord_user_update"])
        self.workflow.add_node("discord_user_delete", discord_tool_map["discord_user_delete"])

        self.workflow.add_node("discord_router", discord_tool_router)

        self.workflow.set_entry_point("agent")

        self.workflow.add_conditional_edges(
            "agent",
            tc,
            {
                "tools": "tools_execution",
               "__end__": "__end__",
            },
        )
        self.workflow.add_edge("tools_execution", "discord_router")

        self.workflow.add_conditional_edges(
            "discord_router",
            discord_tool_router,
            {
                "discord_user_create": "discord_user_create",
                "discord_user_update": "discord_user_update",
                "discord_user_delete": "discord_user_delete",
                "__end__": "__end__",
            },
        )

        # After discord notification, return to agent
        self.workflow.add_edge("discord_user_create", "agent")
        self.workflow.add_edge("discord_user_update", "agent")
        self.workflow.add_edge("discord_user_delete", "agent")

        # Compile the graph
        self.graph = self.workflow.compile(checkpointer=self.memory)

    def get_graph(self):
        return self.graph

    def clear_all_memory(self, config, graph01):
        """Clears the conversation history."""
        state = graph01.get_state(config)
        if state and "messages" in state.values:
            messages = state.values["messages"]
            for msg in messages:
                try:
                    remove_message = RemoveMessage(id=msg.id)
                    graph01.update_state(config, {"messages": remove_message})
                except Exception as e:
                    print(f"Error removing message: {e}")
                    raise



# if __name__ == "__main__":
#     g = workflow()
#     graph = g.get_graph()
#     config = RunnableConfig(configurable={"thread_id": "test-session"})

#     print("Type 'exit' or 'quit' to end the session.\n")

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break

#         response = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

#         messages = response.get("messages", [])
#         if messages:
#             last_message = messages[-1]
#             print(f"Agent: {last_message.content}\n")
#         else:
#             print("⚠️ No response generated.\n")
