FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -U git+https://github.com/Pycord-Development/pycord
RUN chmod +x start.sh
EXPOSE 8080
CMD ["bash", "start.sh"]
