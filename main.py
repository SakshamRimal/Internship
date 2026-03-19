from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controllers import post_controller, user_controller
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await  init_db()   # no await because it is synchronous
    yield       # application runs here it pauses the function

app = FastAPI(lifespan=lifespan)
app.include_router(post_controller.router)
app.include_router(user_controller.router)