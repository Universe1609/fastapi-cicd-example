from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import notes, ping
from app.db import engine, metadata, database
from dotenv import load_dotenv
import os


load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "")
print(DATABASE_URL)
print(f"Conexion a la base de datos: {DATABASE_URL}")
metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@asynccontextmanager
async def db():
    try:
        print("Starting up...")
        await database.connect()
        yield
    finally:
        print("Shutting down...")
        await database.disconnect()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
