FROM python:3.11-slim
WORKDIR /app
COPY .env ./
COPY config.py ./
COPY api/ ./api/
COPY db/ ./db/
COPY bot/requirements.txt ./
RUN python -m .venv .venv && \
    source .venv/bin/activate
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "-m", "api.main"]
