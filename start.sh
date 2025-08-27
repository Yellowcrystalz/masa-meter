#!/usr/bin/env sh

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

trap 'cleanup; exit 0' EXIT INT TERM

while true; do
    if ! kill -0 $BOT_PID 2>/dev/null; then
        break
    fi
    if ! kill -0 $WEBAPP_PID 2>/dev/null; then
        break 
    fi
    sleep 1
done

cleanup
echo "Exit Successful"
