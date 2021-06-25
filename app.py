import json
from fastapi import FastAPI
from data import StarData
from info import Info

app = FastAPI()
data = StarData()
info = Info()


@app.get("/db_info")
def get_db_info(api: str):
    if api == info.api_key:
        return data.data
