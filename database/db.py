from sqlalchemy import create_engine


def connect_to_db():
    """
    Connects to the MySQL database using SQLAlchemy.
    Returns the engine object.
    """
    engine = create_engine('mysql+mysqldb://root:Dhruvvurhd%40777@localhost/onehack_db', echo=True)
    engine.connect()
    return engine



