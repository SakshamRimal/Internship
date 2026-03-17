from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

# Import all models to register them with SQLModel.metadata

# after importing, it automatically bind it in database and create table
from app.models.post_model import Posts

DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost:3306/fastAPI"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Initialize database
def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database connected successfully")

# Session dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]