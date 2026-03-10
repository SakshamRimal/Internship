
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controller.user_controller import router as user_router
from app.auth.auth import authRouter
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(authRouter, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)