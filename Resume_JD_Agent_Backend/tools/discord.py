import sys 
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import os
import requests
from typing import TypedDict, Dict
from dotenv import load_dotenv
from langchain_core.tools import StructuredTool

load_dotenv()


class DiscordMessageTool:
    """Tool for sending Discord messages about candidate DB events."""

    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def send_discord_notification(self, first_name: str, last_name: str, resume: str) -> Dict[str, str]:
        message = f"""
        :green_square:  New Candidate Inserted:
        -------------------
        Candidate Name: {first_name} {last_name}
        Candidate Resume: {resume}
        -------------------
        """
        return self._send_to_discord(message, f"{first_name} (INSERT)")

    def send_discord_notification_Updated(self, first_name: str, last_name: str, resume: str) -> Dict[str, str]:
        message = f"""
        :yellow_square:  Candidate Updated:
        -------------------
        Candidate Name: {first_name} {last_name}
        Candidate Resume: {resume}
        -------------------
        """
        return self._send_to_discord(message, f"{first_name} (UPDATE)")

    def send_discord_notification_delete(self, first_name: str, last_name: str) -> Dict[str, str]:
        message = f"""
        :red_square:  Candidate Deleted:
        -------------------
        Candidate Name: {first_name} {last_name}
        -------------------
        """
        return self._send_to_discord(message, f"{first_name} (DELETE)")

    def _send_to_discord(self, message: str, action_label: str) -> Dict[str, str]:
        try:
            payload = {"content": message}
            response = requests.post(self.webhook_url, json=payload, headers={'Content-Type': 'application/json'})
            print(response.status_code)
            print(response.text)
            return {"Response": f"Candidate {action_label} notified on Discord successfully!"}
        except Exception as e:
            print(f"Error: {str(e)}")
            return {"Error": str(e)}


# if __name__ == "__main__":
#     # Create an instance of the insert tool
#     discord = DiscordMessageTool()
    
#     # Test Case 1: Inserting a candidate with a general description
#     results = discord.send_discord_notification("John", "Doe", "Software Developer at TechCorp")
#     print("Test Case 1 Results:", results)
    
