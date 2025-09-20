# MIT License
#
# Copyright (c) 2025 Justin Nguyen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Defines the API endpoints for serving HTML pages and JSON data from database

This module defines and runs the API service and also serves the frontend static
files. It provides endpoints for both HTML pages and JSON data retrieved from
the database including meter readings, user history, and leaderboard statistics.
Static frontend assets are served with cache-busting support to ensure the
latest versions are loaded.

Examples:
    To run the app using Uvicorn in production:

        uvicorn api.main:app --host 0.0.0.0 --port 8080

    To run the app in development mode:

        uvicorn api.main:app --reload
"""

import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests

from sqlalchemy import Result

from db.crud import (
    get_achievements as crud_get_achievements,
    get_history as crud_get_history,
    get_leaderboard as crud_get_leaderboard,
    get_meter as crud_get_meter
)
from db.database import get_session


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "https://masameter.xyz"
    ],
)


@app.get("/api/meter")
def get_meter() -> list[dict]:
    """Retrieve meter data from the database.

    Returns:
        A list with one element containing the meter data wrapped in a
        dictionary.
    """

    with get_session() as session:
        result: int = crud_get_meter(session)

    return [{"meter": result}]


@app.get("/api/history")
def get_history() -> list[dict]:
    """Retrieve history record of the MasaMention table from database.

    Returns:
        A list of dictionaries with each entry containing:
            id (int):
                Unique primary key of the MasaMention entry.
            date (str):
                ISO formatted string representation of the date in UTC.
            username (str):
                Discord username of the Speaker attached to the entry.
    """

    with get_session() as session:
        results: Result = crud_get_history(session)

    history: list[dict] = []

    for date, username in results:
        history.append({
            "date": date,
            "username": username
        })

    return history


@app.get("/api/leaderboard")
def get_leaderboard() -> list[dict]:
    """Retrieve the Speaker's with the most MasaMention entries.

    Leaderboard is ordered from most to fewest entries.

    Returns:
        A list of dictionaries with each entry containing:
            username (str): Discord usernmae of the Speaker.
            count (int): Number of MasaMention entries attached to the Speaker.
    """

    with get_session() as session:
        results: Result = crud_get_leaderboard(session)

    leaderboard: list[dict] = []

    for username, count in results:
        leaderboard.append({
            "username": username,
            "count": count
        })

    return leaderboard

@app.get("/api/achievements")
def get_achievements() -> list[dict]:
    """
    """

    with get_session() as session:
        achievements_list: list[str] = (
            crud_get_achievements(session)
        )
    
    achievements: list[dict] = []

    achievements.append({
        "achievement_name": "Masa Master",
        "description": "Who said it the most!",
        "emoji": "\U0001F451",
        "username": achievements_list[0]
    })
    achievements.append({
        "achievement_name": "Silent Sashimi",
        "description": "Who said it the least!",
        "emoji": "\U0001F64A",
        "username": achievements_list[1]
    })
    achievements.append({
        "achievement_name": "Tempura Titan",
        "description": "Who said it the most in one day!",
        "emoji": "\U0001F364",
        "username": achievements_list[2]
    })
    achievements.append({
        "achievement_name": "Nigiri Ninja",
        "description": "Who is the only one to say it on a certain day!",
        "emoji": "\U0001F977",
        "username": achievements_list[3]
    })
    achievements.append({
        "achievement_name": "Special Sushi",
        "description": "Who said it on yellowcrystalz's birthday!",
        "emoji": "\U0001F363",
        "username": achievements_list[4]
    })
    
    return achievements 

@app.get("/api/sushi-pic")
def get_sushi_pic():
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": "sushi art",
        "per_page": 50
    }

    try:
        response = requests.get(PEXELS_URL, headers=headers, params=params)
        data = response.json()
        photo = random.choice(data["photos"])
        url = photo["src"]["medium"]

        return {"sushi_pic_url": url}

    except:
        return {"error": "Failed to fetch sushi picture from Pexels"}
