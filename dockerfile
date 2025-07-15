FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]


