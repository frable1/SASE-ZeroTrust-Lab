# Use a Python image read
FROM python:3.12-slim

# Set the working directory in container
WORKDIR /app

# Copy the requirements in the current directory and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary code - core and gateway
# Note: We copy core because gateway/main.py imports it
COPY core/ ./core/
COPY gateway/ ./gateway/

# Exposes the port of the Gateway
EXPOSE 8000

# Command to start the gateway
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]