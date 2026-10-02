FROM python:3.12-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]