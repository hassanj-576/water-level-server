from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import json
import os
from auth import auth_required

app = FastAPI()

DATA_FILE = "data.json"


class ValueModel(BaseModel):
    value: float


def read_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get('value')
    except (json.JSONDecodeError, KeyError):
        return None


def write_data(value: float):
    with open(DATA_FILE, 'w') as f:
        json.dump({'value': value}, f)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/water-level")
async def store_water_level(value_data: ValueModel, auth: bool = Depends(auth_required)):
    write_data(value_data.value)
    return {"message": "Water level stored successfully", "value": value_data.value}


@app.get("/water-level")
async def get_water_level(auth: bool = Depends(auth_required)):
    value = read_data()
    if value is None:
        raise HTTPException(status_code=404, detail="No water level data found")
    return {"value": value}
