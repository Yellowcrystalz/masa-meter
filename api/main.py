from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import FRONTEND_DIR, HTML_DIR, INDEX_PATH

from api.cache_busting import apply_cache_busting

from db.crud import (
    get_history as crud_get_history,
    get_leaderboard as crud_get_leaderboard,
    get_meter as crud_get_meter
)

from db.database import get_session


app = FastAPI()
app.mount("/static", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    html_content = apply_cache_busting(INDEX_PATH.read_text())

    return HTMLResponse(html_content)


@app.get("/html/{file_name}", response_class=HTMLResponse)
def serve_html(file_name: str):
    html_file = HTML_DIR / file_name

    if not html_file.exists() or html_file.suffix != ".html":
        return HTMLResponse("File not found", status_code=404)

    html_content = apply_cache_busting(html_file.read_text())

    return HTMLResponse(html_content)


@app.get("/api/meter")
def get_meter() -> list:
    with get_session() as session:
        results = crud_get_meter(session)

    return [{"meter": results}]


@app.get("/api/history")
def get_history() -> list:
    with get_session() as session:
        results = crud_get_history(session)

    history = []

    for id, date, username in results:
        history.append({
            "id": id,
            "date": date,
            "username": username
        })

    return history


@app.get("/api/leaderboard")
def get_leaderboard() -> list:
    with get_session() as session:
        results = crud_get_leaderboard(session)

    leaderboard = []

    for username, count in results:
        leaderboard.append({
            "username": username,
            "count": count
        })

    return leaderboard
