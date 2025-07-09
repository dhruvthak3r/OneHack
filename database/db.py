from sqlalchemy import create_engine


def connect_to_db():
    """
    Connects to the MySQL database using SQLAlchemy.
    Returns the engine object.
    """
    try:
        engine = create_engine(
            'mysql+mysqldb://admin:Dhruvvurhd777@onehack-1.cdumuk2o669e.ap-south-1.rds.amazonaws.com:3306/onehack', 
            echo=True
        )
        engine.connect()
        
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")