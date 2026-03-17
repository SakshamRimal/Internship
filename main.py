from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controllers import post_controller
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()   # no await because it is synchronous
    yield       # application runs here

app = FastAPI(lifespan=lifespan)
app.include_router(post_controller.router)
