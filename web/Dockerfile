FROM python:3.11-slim

RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Generate self-signed certificate
RUN mkdir /certs && \
    openssl req -x509 -newkey rsa:4096 -keyout /certs/key.pem -out /certs/cert.pem \
    -days 365 -nodes -subj "/CN=localhost"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates

EXPOSE 443

CMD ["python", "app.py"]