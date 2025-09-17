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

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import Result

from config import FRONTEND_DIR, HTML_DIR, INDEX_PATH

from api.cache_busting import apply_cache_busting
from db.crud import (
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
        "http://localhost:3000",
        "http://localhost:5173"
    ],
)


# @app.get("/", response_class=HTMLResponse)
# def index():
#     """Serve the main index page with dynamic cache-busting.
# 
#     Returns:
#         Renedered index page with cache-busting applied to static files.
#     """
# 
#     html_content: str = apply_cache_busting(INDEX_PATH.read_text())
# 
#     return HTMLResponse(html_content)
# 
# 
# @app.get("/html/{file_name}", response_class=HTMLResponse)
# def serve_html(file_name: str):
#     """Serve a requested HTML file with cache-busting applied
# 
#     Args:
#         file_name: Name of the HTML file being requested.
# 
#     Returns:
#         Renedered index page with cahce-busting applied to static files if it
#         exist; otherwise a 404 response.
#     """
# 
#     html_file: Path = HTML_DIR / file_name
# 
#     if not html_file.exists() or html_file.suffix != ".html":
#         return HTMLResponse("File not found", status_code=404)
# 
#     html_content: str = apply_cache_busting(html_file.read_text())
# 
#     return HTMLResponse(html_content)


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
