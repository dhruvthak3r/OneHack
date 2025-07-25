FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh .
RUN chmod +x start.sh

COPY . .

ENV PYTHONPATH=/app

CMD ["sh", "./start.sh"]
