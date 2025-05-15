import sys
import os
from typing import Dict, TypedDict
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from CockroachDB.cockroachDB import CockroachDBAgent
from tools.discord import DiscordMessageTool  # Optional if needed

# Define input schema for structured tool compatibility
class DeleteInput(TypedDict):
    id: str
    firstName : str
    lastName : str

class Delete:
    def __init__(self, connection_string: str):
        """
        Initialize Delete tool with a connection to CockroachDB.
        """
        self.connection_string = connection_string
        self.db = CockroachDBAgent(self.connection_string)
        self.discord = DiscordMessageTool().send_discord_notification_delete  # Optional

    def delete_candidate(self, id: str, firstName, lastName) -> Dict[str, str]:
        """
        Delete a candidate from the database using their ID.
        """
        print(f"Deleting candidate {firstName + " " + lastName} with ID: {id}")
        self.db.connect()
        deleted = self.db.delete_candidate(id)

        if deleted is None:
            message = "Candidate successfully deleted."
        else:
            message = "Cannot find data with the given ID."

        return {"Response": message}

    def delete_candidate_wrapper(self, input_data: DeleteInput) -> Dict[str, str]:
        """
        Wrapper function for delete_candidate.
        """
        db_result = self.delete_candidate(input_data["id"], input_data["firstName"], input_data["lastName"])

        # Optional: notify via Discord
        discord_result = self.discord( input_data["firstName"], input_data["lastName"])
        return {"Response": [db_result, discord_result]}
