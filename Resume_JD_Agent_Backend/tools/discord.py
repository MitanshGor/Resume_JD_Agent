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
        This is the tool that will be used to send the message to the discord channel itself when new candidate is inserted into the database.
        """
        # This is the message that will be sent to the discord channel
        message = f"""
        :green_square:  New Candidate Inserted:
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
            return { "Response": "Candidate with description '{firstname}' (INSERT into DB) notified discord successfully!"}
        except Exception as e:
            print(f"Error: {str(e)}")


    def send_discord_notification_delete(self, first_name: str, last_name: str) : 
        """
        This is the tool that will be used to send the message to the discord channel itself when new candidate is deleted from the database.
        """
        # This is the message that will be sent to the discord chan nel
        message = f"""
        :red_square:  Candidate Deleted:
        -------------------
        Candidate Name: {first_name} {last_name}
        -------------------
        """
        try:
            payload = {"content": message}
            response = requests.post(self.webhook_url, json=payload, headers={'Content-Type': 'application/json'})
            # response.raise_for_status()
            print(response.status_code)
            print(response.text)
            return { "Response": "Candidate with description '{firstname}' (Delete from DB) notified discord successfully!"}
        except Exception as e:
            print(f"Error: {str(e)}")

    def send_discord_notification_Updated(self, first_name: str, last_name: str,  resume: str) : 
        """
        This is the tool that will be used to send the message to the discord channel itself when existing candidate is updated in the database.
        """
        message = f"""
        :yellow_square:  Candidate Updated:
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
            return { "Response": "Candidate with description '{firstname}' (update from DB) notified discord successfully!"}
        except Exception as e:
            print(f"Error: {str(e)}")


# if __name__ == "__main__":
#     # Create an instance of the insert tool
#     discord = DiscordMessageTool()
    
#     # Test Case 1: Inserting a candidate with a general description
#     results = discord.send_discord_notification("John", "Doe", "Software Developer at TechCorp")
#     print("Test Case 1 Results:", results)
    
