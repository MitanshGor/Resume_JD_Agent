import sys 
import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from CockroachDB.cockroachDB import CockroachDBAgent


class retrive: 
    def __init__(self, connection_string): 
        self.connection_string = connection_string
        self.db = CockroachDBAgent(self.connection_string)

    def retrive(self) -> Dict[str, str]:
        """
        Retrieve the candidate data from the database based on the description.
        """
        # Placeholder for actual database retrieval logic
        # In a real implementation, this would query the database and return the result
        self.db.connect()
        retrived_data = self.db.get_candidates()
        return {
            "Retrived Data" : retrived_data
        }
    
if __name__ == "__main__":
    ret= retrive(os.getenv("DATABASE_URL"))
    testing = ret.retrive()
    print(testing)
    