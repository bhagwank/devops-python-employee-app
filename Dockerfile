FROM python:3.12-slim

WORKDIR /app

# Create a non-root user
RUN useradd --create-home appuser

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code as root-owned, read-only for appuser
COPY app.py ./
COPY templates/ ./templates/

# Give application user write permission only to runtime directory
RUN mkdir -p /app/data && \
    chown appuser:appuser /app/data && \
    chmod -R a-w /app && \
    chmod u+w /app/data

# Run as non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
