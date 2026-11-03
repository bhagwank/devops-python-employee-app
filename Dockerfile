FROM python:3.12-slim

WORKDIR /app

# Create a non-root application user
RUN useradd --create-home appuser && \
    chown appuser:appuser /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only the files required to run the application
COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser templates/ ./templates/

# Run application as non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
