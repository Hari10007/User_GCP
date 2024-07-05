from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector

# Replace with your actual database credentials and instance connection name
DB_USER = "postgres"
DB_NAME = "user_crud"
DB_HOST = 'crud-user-428512:asia-south1:user-crud'
DB_PASSWORD = 'password'

def init_connection_engine(connector: Connector) -> create_engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres
    using the Cloud SQL Python Connector with Automatic IAM Database Authentication.
    """
    instance_connection_name = DB_HOST
    db_user = DB_USER
    db_name = DB_NAME

    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",  # Use pg8000 as the dialect for the PostgreSQL connector
            user=db_user,
            db=db_name,
            password=DB_PASSWORD,
            enable_iam_auth=True,  # Enable IAM Database Authentication
        )
        return conn

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    return engine

# Create an instance of the Connector
connector = Connector()

# Initialize the SQLAlchemy engine using the Connector
engine = init_connection_engine(connector)

# Create a SessionLocal instance for Dependency Injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()
