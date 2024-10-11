from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers.messages import message_router
from routers.users import auth_router
from routers.friends import friends_router
from mongo_db import startup_db_client


# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    # await shutdown_db_client(app)


app = FastAPI(
    title="Cheeper",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(friends_router)
app.include_router(message_router)


origins = [
    "http://localhost",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
