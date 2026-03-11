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
        # in engine, it will create the engine for the database so that we can interact it with the database
        SQLModel.metadata.create_all(engine)
        print("Database created successfully")
    except Exception as e:
        print("Database creation failed:", e)


# these are the fixed tiers — they are always seeded on startup and cannot be changed by users
def seed_default_tiers():
    from app.db.models.user import UserTiers

    # these 3 tiers are fixed and will always exist in the database
    fixed_tiers = [
        {"tier_name": "Bronze", "daily_limit": 1000, "transaction_fee": 5},
        {"tier_name": "Silver", "daily_limit": 5000, "transaction_fee": 3},
        {"tier_name": "Gold",   "daily_limit": 20000, "transaction_fee": 1},
    ]

    session = Session(engine)
    try:
        for tier_data in fixed_tiers:
            # only insert if the tier doesn't already exist
            existing = session.query(UserTiers).filter_by(tier_name=tier_data["tier_name"]).first()
            if not existing:
                tier = UserTiers(**tier_data)
                session.add(tier)
        session.commit()
        print("Default tiers seeded successfully")
    except Exception as e:
        session.rollback()
        print("Seeding tiers failed:", e)
    finally:
        session.close()


# a session is what store the object memory so that we dont need to use it again and again
# store object in memory and keeps track of changes needed in data
def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        session.rollback()
        print("Database transaction failed:", e)
        raise e
    # propagate exception to FastAPI
    # use logger instead
    #custom exception
    finally:
        session.close()  # ensure session is closed in all cases

# depends on is used for dependency injection
SessionDep = Annotated[Session , Depends(get_session)]