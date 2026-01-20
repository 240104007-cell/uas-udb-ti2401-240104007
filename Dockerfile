# Gunakan base image Python 3.10 slim
FROM python:3.10-slim

# Set working directory di container
WORKDIR /app

# Copy file requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project ke container
COPY . .

# Tentukan port yang digunakan Cloud Run
ENV PORT 8080

# Jalankan Flask app
CMD ["python", "app.py"]

