from pydantic import BaseModel
from typing import Optional, Dict


class InsertItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    insert_data: dict


class UpdateItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    conditions: dict
    new_data: Dict[str, dict]


class DeleteItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    condition: str


class SelectItem(BaseModel):
    key: str
    db_name: str
    table_name: str
    select_parameter: list
    other: Optional[str] = None
