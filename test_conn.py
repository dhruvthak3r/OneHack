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
        print("Database connection established successfully.")
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")


connect_to_db()

