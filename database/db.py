from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv()

import os
def connect_to_db():
    """
    Connects to the MySQL database using SQLAlchemy.
    Returns the engine object.
    """
    try:
        db_url = os.getenv('aws_rds_url')
        if db_url is None:
            raise ValueError("Environment variable 'aws_rds_url' is not set.")
        engine = create_engine(
            db_url, 
            echo=True
        )
        engine.connect()
        
        return engine
    
    except Exception as e:
        print(f"Error connecting to the database: {e}")



from prefect.blocks.system import Secret

def get_db_connection_for_prefect():
    try:
        secret = Secret.load("aws-rds-url")
        assert isinstance(secret, Secret)
        db_url = secret.get()
        engine = create_engine(db_url, echo=True)
        engine.connect()
        print("Database connection established successfully.")
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

