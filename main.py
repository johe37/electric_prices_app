import json
import datetime
import httpx

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.api import router as api_router
from  routes.pages import router as pages_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes from other files
app.include_router(api_router)
app.include_router(pages_router)
