from fastapi import FastAPI
from .routers import moderation

app = FastAPI()
app.include_router(moderation.router)