from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime
import pytz
from auth import auth_required

app = FastAPI()

DATA_FILE = "data/data.json"


class ValueModel(BaseModel):
    value: float


def read_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, KeyError):
        return None


def write_data(value: float):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    pakistan_tz = pytz.timezone('Asia/Karachi')
    current_time = datetime.now(pakistan_tz)
    
    data = {
        'value': value,
        'timestamp': current_time.isoformat()
    }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/water-level")
async def store_water_level(value_data: ValueModel, auth: bool = Depends(auth_required)):
    write_data(value_data.value)
    pakistan_tz = pytz.timezone('Asia/Karachi')
    current_time = datetime.now(pakistan_tz)
    return {
        "message": "Water level stored successfully", 
        "value": value_data.value,
        "timestamp": current_time.isoformat()
    }


@app.get("/water-level")
async def get_water_level(auth: bool = Depends(auth_required)):
    data = read_data()
    if data is None:
        raise HTTPException(status_code=404, detail="No water level data found")
    return {
        "value": data.get("value"),
        "timestamp": data.get("timestamp")
    }
