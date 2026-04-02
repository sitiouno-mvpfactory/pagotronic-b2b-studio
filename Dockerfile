FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY index.html ./index.html

EXPOSE 8080

CMD ["uvicorn", "product_app.webapp:app", "--host", "0.0.0.0", "--port", "8080"]
