import json
import datetime
import httpx

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.api import router as api_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes from other files
app.include_router(api_router)


@app.get("/")
async def index(request: Request):
  today = datetime.date.today()
  price_class = "SE3"

  url = f"https://www.elprisetjustnu.se/api/v1/prices/{today:%Y/%m-%d}_{price_class}.json"

  async with httpx.AsyncClient() as client:
    resp = await client.get(url)
    resp.raise_for_status()

  data = resp.json()

  prices = [d["SEK_per_kWh"] for d in data]
  times = [
    datetime.datetime.fromisoformat(d["time_start"]).strftime("%H:%M")
    for d in data
  ]

  return templates.TemplateResponse(
    "index.html",
    {
      "request": request,
      "prices": prices,
      "times": times,
      "date": today.strftime("%Y-%m-%d"),
      "price_class": price_class,
    }
  )

@app.get("/sample", response_class=HTMLResponse)
async def read_sample(request: Request):
  try:
    with open("sample_data.json") as f:
      data = json.load(f)

    prices = [d["SEK_per_kWh"] for d in data]
    times = [
      datetime.datetime.fromisoformat(d["time_start"]).strftime("%H:%M")
      for d in data
    ]

    return templates.TemplateResponse(
      "sample.html",
      {
        "request": request,
        "prices": prices,
        "times": times
      }
    )

  except Exception as e:
    return HTMLResponse(
      content=f"<h1>Fel</h1><p>{e}</p>",
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.get("/prices", response_class=HTMLResponse)
async def read_prices(request: Request):
  return templates.TemplateResponse(
    "prices.html",
    {"request": request}
  )
