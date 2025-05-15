from tools.insert import insert
from tools.retrival import Retrieve
from tools.delete import Delete
from tools.discord import DiscordMessageTool
from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
import os

load_dotenv()


class Tools:
    def __init__(self):
        # Load configuration
        db_url = os.getenv("DATABASE_URL")

        # Initialize database logic
        self.insert_tool = insert(db_url).insert_canidate_wrapper
        self.retrieve_tool = Retrieve(db_url).retrieve_candidates
        self.delete_tool = Delete(db_url).delete_candidate


    def get_database_tools(self):
        return [
            StructuredTool.from_function(
                func=self.insert_tool,
                name="insert_user",
                description="Insert a new user. Input: {first_name, last_name, resume}"
            ),
            StructuredTool.from_function(
                func=self.retrieve_tool,
                name="retrieve_user",
                description="Retrieve users based on a query."
            ),
            StructuredTool.from_function(
                func=self.delete_tool,
                name="delete_user",
                description="Delete a user using their ID  OR firstname and lastname."
            ),
        ]
    def toolkit(self):
        tools = self.get_database_tools()
        return tools
