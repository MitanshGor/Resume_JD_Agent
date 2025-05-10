
from tools.insert import insert
from tools.retrival import retrive
from tools.delete import delete
import os 
from tools.discord import DiscordMessageTool
from dotenv import load_dotenv

load_dotenv()
class tools:


    def database_tool(self):
        # This is for the connection string for the database -> The only connection string that is needed to
        # Connect to CoackRaochDB
        self.db_connection = os.getenv("DATABASE_URL")

        # Creating the instances of both the retrival and insert tools
        self.insert_tool = insert(self.db_connection)
        self.retrival_tool = retrive(self.db_connection)
        self.delete_tool = delete(self.db_connection)
        

        # Building the services that will be used to invoke the tools itself
        self.insert = self.insert_tool.insert_canidate
        self.retrive = self.retrival_tool.retrive
        self.delete = self.delete_tool.delete

        return [self.insert, self.retrive, self.delete, self.discord_tool]

    def discord_tool(self):
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        # Creating the instances of both the retrival and insert tool
        self.discord_tool = DiscordMessageTool()

        # Building the services that will be used to invoke the tools itself
        self.discord_notification = self.discord_tool.send_discord_notification

        return [self.discord_notification]
    def __init__(self): 
        database_tools = self.database_tool()
        discord_tools = self.discord_tool()
        self.tools_list = database_tools + discord_tools

    def toolkit(self): 
        return self.tools_list
    
# if __name__ == "__main__":
#     tools = tools()
#     li = tools.toolkit()
#     testing = li[1] 
#     print(testing())
#     testing = li[2]("1067972559791915009")
#     print(testing)