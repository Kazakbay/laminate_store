FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
# Copy requirements.txt and main.py from the project root
COPY deployment/docker/requirements.txt ./requirements.txt

COPY main.py ../..

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
