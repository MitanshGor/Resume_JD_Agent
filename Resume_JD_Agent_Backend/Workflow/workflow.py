import os
import sys
from dotenv import load_dotenv
# from langchain_ollama import OllamaEmbeddings
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition as tc
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langgraph.prebuilt import ToolNode
import json

# Set up system path for local imports
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tools.utility import Tools
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



class workflow:
    def __init__(self):
        self.memory = MemorySaver()
        self.flow = StateGraph(AgentState)
        self.graph = None
        # embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.single_agent = Agent()
        # Register tools and enhanced ToolNode
        self.tools = ToolNodeWithTracking(Tools().toolkit())
        self.workflow_init()
        self.clear = self.clear_all_memory

    def workflow_init(self):
        self.flow.add_node("agent", self.single_agent.run_agent)
        tool_map = {
            tool.name: tool for tool in Tools().toolkit()
        }        


        def dynamic_tool_executor(state):
            messages = state.get("messages", [])
            if not messages:
                raise ValueError("No messages in state.")

            ai_message = messages[-1]
            tool_calls = ai_message.tool_calls
            new_messages = []

            for tool_call in tool_calls:
                name = tool_call["name"]
                args = tool_call["args"]
                tool_id = tool_call["id"]
                try:
                    tool_result = tool_map[name].invoke(args)

                    # Extract a clean string message
                    content = ""
                    if isinstance(tool_result, dict):
                        response_value = tool_result.get("Response", tool_result)
                        if isinstance(response_value, list):
                            content = "\n".join(item.get("Response", str(item)) for item in response_value)
                        else:
                            content = str(response_value)
                    else:
                        content = str(tool_result)

                    # ✅ Add as tool message
                    new_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": content
                    })

                except Exception as e:
                    print(f"Error invoking tool '{name}': {e}")
                    raise

            print('---------------------------------------------------')
            print('MESSAGE 1  : ',  messages)
            print('---------------------------------------------------')
            print('MESSAGE 2 : ', new_messages)
            print('---------------------------------------------------')
            
            return {
                "messages": messages + new_messages,
            }




        self.flow.add_node("tools_execution", dynamic_tool_executor)
        # Entry point
        self.flow.set_entry_point("agent")
        self.flow.add_conditional_edges(
            "agent",
            tc,
            {
                "tools": "tools_execution",
                 "end": "__end__"
            },
        )

        self.flow.add_edge("tools_execution", "agent")

        # Compile the graph
        self.graph = self.flow.compile(checkpointer=self.memory)

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
