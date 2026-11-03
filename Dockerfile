FROM python:3.12-slim

WORKDIR /app

# Create non-root application user
RUN useradd --create-home appuser

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (root-owned by default)
COPY app.py ./
COPY templates/ ./templates/

# Create writable directory for SQLite database
RUN mkdir -p /app/data && \
    chown appuser:appuser /app/data && \
    chmod 755 /app/data

# Configure database location inside Docker
ENV DATABASE_PATH=/app/data/employees.db

# Run application as non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
