#!/usr/bin/env bash

set -e

echo "Starting Discord Bot"
python -m bot.main &
BOT_PID=$!

echo "Starting Web App"
uvicorn api.main:app --host 0.0.0.0 --port 8080 &
WEBAPP_PID=$!

cleanup() {
    echo "Stopping bot and API..."
    [[ -n "$BOT_PID" ]] && kill "$BOT_PID" 2>/dev/null || true
    [[ -n "$WEBAPP_PID" ]] && kill "$WEBAPP_PID" 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM
wait -n $BOT_PID $WEBAPP_PID
echo "Exit Successful"
