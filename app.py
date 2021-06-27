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


@app.get("/easy_get")
def get_value(api: str, db_name: str, table_name: str, name: str, value):
    return data.easy_get(api, db_name, table_name, name, value)


@app.get("/easy_get_all")
def get_all_items(api: str, db_name: str, table_name: str):
    return data.get_all_items(api, db_name, table_name)


@app.post("/east_set")
def easy_set(item: EasySet, api: str):
    return data.easy_set(item, api)
