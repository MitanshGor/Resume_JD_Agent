import sys 
import os
from typing import Dict, TypedDict
import psycopg2
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from CockroachDB.cockroachDB import CockroachDBAgent
from tools.discord import DiscordMessageTool

class InsertInput(TypedDict):
    first_name: str
    last_name: str
    query: str
    llmResult : object

class DeleteInput(TypedDict):
    id: str


class insert: 
    def __init__(self, connection_string): 
        self.connection_string = connection_string
        # Establishing the connection for the coackroachDB
        self.db = CockroachDBAgent(self.connection_string)
        self.discord = DiscordMessageTool().send_discord_notification

    # Tool that is used to help insert the data into the database
    def insert_canidate(self, first_name: str, last_name: str, query: str) -> Dict[str, str]:
        """  Insert a candidate into the database.   """

        print(first_name , last_name, query)
        # WE need to hardcode the connection just so the agent can will be able to connect to the database itself
        self.db.connect()
        
        self.db.insert_candidate(first_name, last_name, query)
        return { "Response": f"Candidate with description '{query}' inserted successfully!" }

    def insert_canidate_wrapper(self, input_data: InsertInput) -> Dict[str, str]:
        """
        Wrapper function to call the insert_candidate method.

        Args:
            first_name (str): Candidate's first name
            last_name (str): Candidate's last name
            query (str): Candidate's job-related query or description
            llmResult (object): A structured evaluation object containing committee-based scores, improvement tips, strengths, and an overall score summarizing a candidate’s fit for a job role.


        Returns:
            Dict[str, str]: Confirmation message
        """
        dbResult = self.insert_canidate(input_data['first_name'], input_data['last_name'], input_data['llmResult'])
        discord_result = self.discord(input_data['first_name'], input_data['last_name'], input_data['llmResult'])


        return {"Response" : [dbResult, discord_result]}


# if __name__ == "__main__":
#     # Create an instance of the insert tool
#     insert_tool = insert(os.getenv("DATABASE_URL"))
    
#     # Test Case 1: Inserting a candidate with a general description
#     results = insert_tool.insert_canidate("John", "Doe", "Software Developer at TechCorp")
#     print("Test Case 1 Results:", results)
    
#     # Test Case 2: Inserting a candidate with a different job title
#     results = insert_tool.insert_canidate("Jane", "Smith", "Product Manager at InnovateX")
#     print("Test Case 2 Results:", results)
    
#     # Test Case 3: Inserting a candidate with a generic title
#     results = insert_tool.insert_canidate("Alice", "Johnson", "Software Engineer")
#     print("Test Case 3 Results:", results)
    
#     # Test Case 4: Inserting a candidate with a unique description
#     results = insert_tool.insert_canidate("Bob", "Taylor", "Data Scientist at DataSciences Inc.")
#     print("Test Case 4 Results:", results)
    
#     # Test Case 5: Inserting a candidate with a specific company name
#     results = insert_tool.insert_canidate("Emily", "Clark", "Marketing Strategist at CloudCo")
#     print("Test Case 5 Results:", results)
