# LangChain SQL Chat - Minimal Learning Version
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import dotenv
dotenv.load_dotenv(".env")

import os

def setup_database():
    """Setup SQLite database connection"""
    db_path = Path(__file__).parent / "student.db"
    creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    return SQLDatabase(create_engine("sqlite:///", creator=creator))

def setup_agent(api_key):
    """Setup LLM and SQL agent"""
    # Initialize LLM
    llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-8b-instant")
    
    # Setup database
    db = setup_database()
    
    # Create toolkit and agent
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, 
                           agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    return agent

def main():
    # Get API key
    api_key = os.environ.get('GROQ_API_KEY', 'your_default_api_key_here')
    
    # Setup agent
    agent = setup_agent(api_key)
    
    # Chat loop
    print("\nSQL Chat started! Type 'quit' to exit.")
    while True:
        query = "how many rows in this table student"
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            response = agent.run(query)
            print(f"\nResponse: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()


        


