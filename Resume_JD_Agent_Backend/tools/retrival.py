import sys 
import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from CockroachDB.cockroachDB import CockroachDBAgent


from typing import Dict, Any

class Retrieve:
    def __init__(self, connection_string: str):
        """
        Initialize Retrieve tool with a connection to CockroachDB.
        """
        self.connection_string = connection_string
        self.db = CockroachDBAgent(self.connection_string)

    def retrieve_candidates(self) -> Dict[str, Any]:
        """
        Retrieve all candidate data from the database.

        Returns:
            Dict[str, Any]: Retrieved candidate data
        """
        self.db.connect()
        retrieved_data = self.db.get_candidates()
        return {
            "retrieved_data": retrieved_data
        }

    
# if __name__ == "__main__":
#     ret= retrive(os.getenv("DATABASE_URL"))
#     testing = ret.retrive()
#     print(testing)
    