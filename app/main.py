from fastapi import FastAPI
from app.api.v1.api import api_router


app = FastAPI(title="starlight")

app.include_router(api_router)
