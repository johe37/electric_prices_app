import json
import datetime

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
def read_root():
    pass

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
