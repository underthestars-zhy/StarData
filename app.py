from fastapi import FastAPI
from data import StarData
from schemas import *

app = FastAPI()
data = StarData()


@app.get("/db_info")
def get_db_info(api: str):
    return data.get_data_info(api)


@app.post("/insert")
def insert(item: InsertItem, api: str):
    return data.insert(item, api)


@app.post("/update")
def update(item: UpdateItem, api: str):
    return data.update(item, api)


@app.post("/delete")
def delete(item: DeleteItem, api: str):
    return data.delete(item, api)


@app.post("/select")
def select(item: SelectItem, api: str):
    return data.select(item, api)
