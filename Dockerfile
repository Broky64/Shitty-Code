# Dockerfile pour exécuter l'application

FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY python/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY python/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
