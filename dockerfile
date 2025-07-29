# Use a slim Python 3.11 base image for a smaller footprint
FROM python:3.11-slim

# Set the app's working directory
WORKDIR /app

# Install needed system tools (like curl for health checks)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main app and CLI files
COPY app.py .
COPY cli.py .

# Create a folder for logs
RUN mkdir -p logs

# Open port 5000 for the API
EXPOSE 5000

# Check if the app is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the LocalAIHub server
CMD ["python", "app.py"]