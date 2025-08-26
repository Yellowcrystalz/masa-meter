#!/usr/bin/env sh

# set -e
# 
# echo "Starting Discord Bot"
# python -m bot.main &
# BOT_PID=$!
# 
# echo "Starting Web App"
# uvicorn api.main:app --host 0.0.0.0 --port 8080 &
# WEBAPP_PID=$!
# 
# cleanup() {
#     echo "Stopping bot and API..."
#     kill $BOT_PID $WEBAPP_PID
#     wait $BOT_PID $WEBAPP_PID 2>/dev/null
#     exit 0
# }
# 
# trap cleanup SIGINT SIGTERM
# 
# wait $BOT_PID $WEBAPP_PID

python -m bot.main
