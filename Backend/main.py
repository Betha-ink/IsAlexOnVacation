import os
import requests
import time

from fastapi import FastAPI
from datetime import datetime

DAWARICH_URL = os.environ["DAWARICH_URL"]
API_KEY = os.environ["API_KEY"]

_cache = {"ts": 0, "value": None}

app = FastAPI()

@app.get("/vacation")
def vacation():

    if time.time() - _cache.get("ts") < 60:
        return {"onVacation": _cache["value"]}

    url = f"{DAWARICH_URL}/api/v1/points"

    response = requests.get(
        url,
        params={"order": "desc",
                "per_page": 1,
                "page": 1},
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=5
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Dawarich API Error: HTTP {response.status_code} - {response.text}") from e

    data = response.json()

    if not data:
        _cache.update(ts=time.time(), value=None)
        return {"onVacation": None}

    point = data[0]

    timestamp = int(point["timestamp"])
    latitude = float(point["latitude"])
    longitude = float(point["longitude"])

    point_date = datetime.fromtimestamp(timestamp)

    if (datetime.now() - point_date).days > 1:
        result = None
    elif is_inside_noe(latitude, longitude):
        result = False
    else:
        result = True

    _cache.update(ts=time.time(), value=result)

    return {"onVacation": result}


def is_inside_noe(latitude, longitude):
    # Area of Lower Austria + Vienna
    MIN_LAT = 47.850456
    MAX_LAT = 48.857389
    MIN_LON = 14.758932
    MAX_LON = 16.955710

    return MIN_LAT <= latitude <= MAX_LAT and MIN_LON <= longitude <= MAX_LON
