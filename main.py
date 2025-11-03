import json


from typing import Union
from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/sample", status_code=200)
def read_sample(response: Response):
    try:
        with open('sample_data.json') as f:
            data = json.load(f)
            return data
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"msg": "Could not load sample data"}
