FROM python:3.11.4-slim

WORKDIR /app

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .

CMD ["panel", "serve", "dashboard.py", "--address", "0.0.0.0", "--port", "5006", "--allow-websocket-origin=*"]

