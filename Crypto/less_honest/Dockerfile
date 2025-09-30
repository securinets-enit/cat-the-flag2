FROM python:3.12-slim

WORKDIR /app

COPY chall.py .
COPY secret.py .

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

EXPOSE 1004

CMD ["socat","-v","-T", "90", "TCP-LISTEN:1004,fork,reuseaddr,bind=0.0.0.0", "EXEC:'python3 chall.py'"]
