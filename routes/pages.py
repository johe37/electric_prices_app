import json
import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.prices import fetch_prices, PriceServiceError

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
  today = datetime.date.today()
  price_class = "SE3"

  try:
    data = await fetch_prices(
      price_class=price_class,
      date=today,
    )
  except PriceServiceError as e:
    return templates.TemplateResponse(
      "error.html",
      {
        "request": request,
        "message": str(e),
      },
      status_code=500,
    )

  prices = [d["SEK_per_kWh"] for d in data]
  times = [
    d["time_start"][11:16]
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

@router.get("/sample", response_class=HTMLResponse)
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


@router.get("/prices", response_class=HTMLResponse)
async def read_prices(request: Request):
  return templates.TemplateResponse(
    "prices.html",
    {"request": request}
  )
