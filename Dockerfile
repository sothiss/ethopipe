# Use a slim Python 3.12 base image
FROM python:3.12-slim

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Set working directory
WORKDIR /app

# Copy packaging configuration and source files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Upgrade pip, install uvicorn for server capability, and install the package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir . uvicorn

# Expose the API port
EXPOSE 8080

# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "ethopipe.api:app", "--host", "0.0.0.0", "--port", "8080"]
