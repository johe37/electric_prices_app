import datetime
import httpx

VALID_PRICE_CLASSES = {
  "SE1": {"city": "Luleå", "location": "Norra Sverige"},
  "SE2": {"city": "Sundsvall", "location": "Norra Mellansverige"},
  "SE3": {"city": "Stockholm", "location": "Södra Mellansverige"},
  "SE4": {"city": "Malmö", "location": "Södra Sverige"},
}


class PriceServiceError(Exception):
  pass


async def fetch_prices(
  *,
  price_class: str,
  date: datetime.date,
) -> list[dict]:
  price_class = price_class.upper()

  if price_class not in VALID_PRICE_CLASSES:
    raise PriceServiceError(f"Invalid price class: {price_class}")

  date_str = date.strftime("%Y/%m-%d")
  url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{price_class}.json"

  async with httpx.AsyncClient() as client:
    resp = await client.get(url)

  if resp.status_code != 200:
    raise PriceServiceError(
      f"Failed to fetch prices ({resp.status_code})"
    )

  return resp.json()
