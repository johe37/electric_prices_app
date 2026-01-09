import datetime
import httpx

from typing import List
from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

@router.get("/hello")
def get_hello():
    return {"Hello": "World"}
