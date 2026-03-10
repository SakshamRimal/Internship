from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import  create_db_and_tables
from app.controllers.auth_controller import auth_router
# execute the code before other task is done we have created a database , session now we have to call the
#method to table
# use context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize DB at start this iss for initializing db at start
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    auth_router ,
    tags=["auth"],
    prefix="/auth"
)



@app.get("/")
async def root():
    return {"message": "Hello World"}

