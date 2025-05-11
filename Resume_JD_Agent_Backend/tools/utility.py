from tools.insert import insert
from tools.retrival import retrive
from tools.delete import delete
from tools.discord import DiscordMessageTool
from dotenv import load_dotenv
from langchain.tools import Tool
import os

load_dotenv()

class tools:
    def __init__(self):
        self.db_connection = os.getenv("DATABASE_URL")
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        # Initialize database handlers
        self.insert_tool = insert(self.db_connection)
        self.retrival_tool = retrive(self.db_connection)
        self.delete_tool = delete(self.db_connection)

        # Initialize Discord tool
        self.discord_tool = DiscordMessageTool(webhook_url=self.discord_webhook_url)

        # Compose the final tools list
        self.database_tools = self._get_database_tools()
        self.discord_tools = self._get_discord_tools()
        self.tools_list = self.database_tools + self.discord_tools

    def _get_database_tools(self):
        """LangChain-compatible tools for database operations"""
        return [
            Tool(
                name="insert_candidate",
                func=self.insert_tool.insert_canidate,
                description="Insert a new candidate into the database. Input should be a JSON with candidate details."
            ),
            Tool(
                name="retrive_candidate",
                func=self.retrival_tool.retrive,
                description="Retrieve a candidate from the database. Input should be a JSON with candidate ID."
            ),
            Tool(
                name="delete_candidate",
                func=self.delete_tool.delete,
                description="Delete a candidate from the database. Input should be a JSON with candidate ID."
            ),
        ]

    def _get_discord_tools(self):
        """LangChain-compatible tools for Discord notifications"""
        return [
            Tool(
                name="discord_user_create",
                func=self.discord_tool.send_discord_notification,
                description="Send a message to Discord when a user is created. Input should be a JSON with keys: first_name, last_name, resume."
            ),
            Tool(
                name="discord_user_update",
                func=self.discord_tool.send_discord_notification_Updated,
                description="Send a message to Discord when a user is updated. Input should be a JSON with keys: first_name, last_name, resume."
            ),
            Tool(
                name="discord_user_delete",
                func=self.discord_tool.send_discord_notification_delete,
                description="Send a message to Discord when a user is deleted. Input should be a JSON with keys: first_name, last_name."
            ),
        ]

    def toolkit(self):
        """Return the full list of tools for the agent"""
        return self.tools_list