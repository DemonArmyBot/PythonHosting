# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

# Expose port (optional, Render ignores)
EXPOSE 5000

CMD ["python", "app.py"]