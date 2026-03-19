from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.logger import logger

# Import all models so they are registered

# Async MySQL URL
DATABASE_URL = "mysql+aiomysql://root:yourpassword@localhost:3306/fastAPI"

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Async session factory
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Initialize database
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database connected successfully")

# Async session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Type annotation for FastAPI
SessionDep = Annotated[AsyncSession, Depends(get_session)]