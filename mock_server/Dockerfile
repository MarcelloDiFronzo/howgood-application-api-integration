FROM python:3.11-slim

WORKDIR /app

COPY mock_server_requirements.txt .
RUN pip install --no-cache-dir -r mock_server_requirements.txt

COPY . .

CMD ["python", "app.py"]
