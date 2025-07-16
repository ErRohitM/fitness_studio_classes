import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import classes

# FastAPI App
app = FastAPI(
    title="Fitness Studio Booking API",
    description="A comprehensive booking system for fitness classes",
    version="1.0.0"
)
allowed_origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classes.router)