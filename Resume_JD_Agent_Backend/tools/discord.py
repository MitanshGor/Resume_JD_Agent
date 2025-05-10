import sys 
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

class DiscordMessageTool:
    """ This is the tool that will be used to send the message to the discord channel itself"""
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
    
    # Tool that is used to help insert the data into the database
    def send_discord_notification(self, first_name: str, last_name: str,  resume: str) : 
        """
        This is the tool that will be used to send the message to the discord channel itself
        """
        # This is the message that will be sent to the discord channel
        message = f"""
        New Candidate Inserted:
        -------------------
        Candidate Name: {first_name} {last_name}
        Candidate Resume: {resume}
        -------------------
        """
        try:
            payload = {"content": message}
            response = requests.post(self.webhook_url, json=payload, headers={'Content-Type': 'application/json'})
            # response.raise_for_status()
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")


# if __name__ == "__main__":
#     # Create an instance of the insert tool
#     discord = DiscordMessageTool()
    
#     # Test Case 1: Inserting a candidate with a general description
#     results = discord.send_discord_notification("John", "Doe", "Software Developer at TechCorp")
#     print("Test Case 1 Results:", results)
    
