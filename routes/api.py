import datetime
import httpx

from typing import List
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

valid_prices_classes = {
    "SE1": {
        "city": "Luleå",
        "location": "Norra Sverige"
    },
    "SE2": {
        "city": "Sundsvall",
        "location": "Norra Mellansverige"
    },
    "SE3": {
        "city": "Stockholm",
        "location": "Södra Mellansverige"
    },
    "SE4": {
        "city": "Malmö",
        "location": "Södra Sverige"
    },
}


@router.get("/hello")
def get_hello():
    return {"Hello": "World"}

@router.get("/prices/{price_class}/{date}", response_model=List[dict])
async def get_prices(price_class: str, date: datetime.date):
    date_str = date.strftime("%Y/%m-%d")
    price_class_str = price_class.upper()

    if price_class_str not in valid_prices_classes:
        raise HTTPException(
        status_code=404,
        detail=f"'{price_class_str}' is not a valid price class. "
                f"Valid values are {', '.join(valid_prices_classes)}"
        )

    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{price_class_str}.json"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise HTTPException(
        status_code=resp.status_code,
        detail="Could not fetch data"
        )

    return resp.json()
