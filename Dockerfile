FROM python:3.11-slim

# Install Ray
RUN pip install --no-cache-dir ray[default]

# Set the working directory
WORKDIR /app

# Expose the necessary ports
EXPOSE 6379 8265 10001 12345

# Default command (can be overridden)
CMD ["ray", "start", "--head", "--dashboard-host=0.0.0.0"]