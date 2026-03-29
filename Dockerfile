# Use a modern, stable Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Minimal system dependencies (removed build-essential and curl to avoid apt-get issues)
# Polars and Streamlit have pre-built wheels, so we rarely need a compiler.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the application
# We use direct command instead of healthcheck to minimize external calls during build/startup
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
