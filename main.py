import json
import httpx
import datetime


from typing import Union
from fastapi import (
    FastAPI,
    Request,
    Response,
    status,
    HTTPException
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")


valid_prices_classes = {
    "SE1": {
        "city": 'Luleå',
        "location": 'Norra Sverige'
    },
    "SE2": {
        "city": 'Sundsvall',
        "location": 'Norra Mellansverige'
    },
    "SE3": {
        "city": 'Stockholm',
        "location": 'Södra Mellansverige'
    },
    "SE4": {
        "city": 'Malmö',
        "location": 'Södra Sverige'
    },
}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/sample", response_class=HTMLResponse)
async def read_sample(request: Request):
    try:
        with open('sample_data.json') as f:
            data = json.load(f)

            prices = [d["SEK_per_kWh"] for d in data]
            times = [d["time_start"] for d in data]
            times = [
              #datetime.datetime.fromisoformat(d["time_start"]).strftime("%Y-%m-%d-%H:%M")
              datetime.datetime.fromisoformat(d["time_start"]).strftime("%H:%M")
              for d in data
            ]
            print(times[0])

            return templates.TemplateResponse("index.html", {
                "request": request,
                "prices": prices,
                "times": times
            })
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Fel</h1><p>Kunde inte läsa sample_data.json: {e}</p>",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/prices/{price_class}/{date}", response_model=List[dict])
async def get_prices(price_class: str, date: datetime.date):
    # price_class for example be "SE3"
    date_str = date.strftime("%Y/%m-%d")
    price_class_str = price_class.upper()

    if price_class_str not in valid_prices_classes.keys():
        raise HTTPException(status_code=404, detail=f"'{price_class_str}' is not a valid price class. Valid value are {', '.join(valid_prices_classes)}")

    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{price_class_str}.json"
    print(url)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        print(resp)
        raise HTTPException(status_code=resp.status_code, detail="Could not fetch data")
    data = resp.json()
    return data
