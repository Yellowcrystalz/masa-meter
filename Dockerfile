FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh
EXPOSE 8080
CMD ["bash", "start.sh"]
