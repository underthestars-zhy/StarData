import error
from fastapi import FastAPI
from data import StarData
from info import info
from pydantic import BaseModel

app = FastAPI()
data = StarData()


class InsertItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    insert_data: dict


@app.get("/db_info")
def get_db_info(api: str):
    if api == info.api_key:
        return data.data
    else:
        return error.ValidationError('Unable to verify API key')


@app.post("/insert")
def insert(item: InsertItem, api: str):
    if api == info.api_key:
        return data.insert(item.dict())
    else:
        return error.ValidationError('Unable to verify API key')


@app.post("/update")
def update(api: str):
    if api == info.api_key:
        return
    else:
        return error.ValidationError('Unable to verify API key')
