from fastapi import FastAPI

from db.crud import (
    get_history as crud_get_history,
    get_leaderboard as crud_get_leaderboard,
    get_meter as crud_get_meter
)

from db.database import get_session


app = FastAPI()


@app.get("/meter")
def get_meter() -> list:
    with get_session() as session:
        results = crud_get_meter(session)

    return [{"meter": results}]


@app.get("/history")
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


@app.get("/leaderboard")
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
