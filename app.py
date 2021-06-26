import error
from fastapi import FastAPI
from data import StarData
from info import info
from pydantic import BaseModel
from typing import Dict

app = FastAPI()
data = StarData()


class InsertItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    insert_data: dict


class UpdateConditions(BaseModel):
    parameter: str
    expression: str
    value: str


class UpdateItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    conditions: Dict[str, UpdateConditions]
    new_data: dict


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
def update(item: UpdateItem, api: str):
    if api == info.api_key:
        return data.update(item.dict())
    else:
        return error.ValidationError('Unable to verify API key')
