# ---------- STAGE 1: Build ----------
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy dependency file first (layer caching)
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# ---------- STAGE 2: Runtime ----------
FROM python:3.10-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app.py .

# Set environment path
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

# Expose backend port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]
