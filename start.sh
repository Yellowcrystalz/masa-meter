#!/usr/bin/env bash

set -e

echo "Starting Discord Bot"
python -m bot.main --prod &
BOT_PID=$!

echo "Starting Web App"
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
WEBAPP_PID=$!

cleanup() {
    echo "Stopping bot and API..."

    kill -TERM "$BOT_PID" 2>/dev/null || true
    kill -TERM "$WEBAPP_PID" 2>/dev/null || true

    wait "$BOT_PID" 2>/dev/null || true
    wait "$WEBAPP_PID" 2>/dev/null || true

    echo "Exit Successful"
}

trap cleanup EXIT INT TERM
wait -n $BOT_PID $WEBAPP_PID
