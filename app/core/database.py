import os
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from typing import Annotated
from sqlmodel import SQLModel, Session

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(mysql_url, echo=True)


def create_db_and_tables():
    try:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        print("Database created successfully")
    except Exception as e:
        print(f"Error creating database: {e}")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]