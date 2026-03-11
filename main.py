from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import create_db_and_tables, seed_default_tiers
from app.controllers.auth_controller import auth_router
from app.controllers.tier_controller import tier_router
from app.controllers.wallet_controller import wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_default_tiers()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(tier_router, tags=["tier"], prefix="/tier")
app.include_router(wallet_router, tags=["wallet"], prefix="/wallet")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")