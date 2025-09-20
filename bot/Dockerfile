FROM python:3.11-slim
WORKDIR /app
COPY .env ./
COPY config.py ./
COPY bot/ ./bot/
COPY db/ ./db/
COPY bot/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "bot.main", "--prod"]