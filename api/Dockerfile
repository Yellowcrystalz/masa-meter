FROM python:3.11-slim
WORKDIR /app
COPY .env ./
COPY config.py ./
COPY api/ ./api/
COPY db/ ./db/
COPY api/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host:", "0.0.0.0", "--port", "8000"]