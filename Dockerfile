FROM python:3.11-slim

ENV PYTHONPATH=/app:/app/src

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app/src
CMD ["python", "flow.py"]

