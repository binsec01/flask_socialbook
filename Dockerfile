FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/uploads

# Set permissions
RUN chmod +x fetcher.py

# Create a non-root user
RUN useradd -m ctfuser
RUN chown -R ctfuser:ctfuser /app
USER ctfuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 