import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import Field , SQLModel, create_engine , Session
from dotenv import load_dotenv

# load .env from the app directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

#load .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# connection string
# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<database>
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"

# this initialized a connection engine to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# this is for database connection it holds the connection to database
# engine is used for holding the connection to database
# startup function to ensure all tables exist
# this is used to ensure if tables and database is connected and instantiated
def create_db_and_tables():
    try:
        # drop old tables first so they get recreated with correct columns
        # remove this line once your schema is stable
        SQLModel.metadata.create_all(engine)
        print("Database created successfully")
    except Exception as e:
        print("Database creation failed:", e)


# a session is what store the object memory so that we dont need to use it again and again
# store object in memory and keeps track of changes needed in data
def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        session.rollback()
        print("Database transaction failed:", e)
        raise e  # propagate exception to FastAPI
    # use logger instead
    #custom exception
    finally:
        session.close()  # ensure session is closed in all cases

# depends on is used for dependency injection
SessionDep = Annotated[Session , Depends(get_session)]