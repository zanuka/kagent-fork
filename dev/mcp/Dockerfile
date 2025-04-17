FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    git \
    ca-certificates \
    curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl (adjusted for amd64; change to arm64 if needed)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8083 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Create and activate virtual environment
RUN python3 -m venv /opt/venv

# Set working directory
WORKDIR /app/python

# Copy requirements first for better caching
COPY python/requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip check && \
    pip show openai && \
    python3 -c "import openai; print('OpenAI version:', openai.__version__)"

# Copy the rest of the application
COPY python/pyproject.toml ./
COPY python/src/ ./src/

# Create README.md file
RUN echo "# Kagent MCP Service\n\nThis service provides the Model Control Plane for Kagent." > README.md

# Install the package in editable mode
RUN pip install -e . && \
    python3 -c "import openai; print('OpenAI still available')"

# Set PYTHONPATH to prioritize site-packages
ENV PYTHONPATH="/opt/venv/lib/python3.11/site-packages:/app/python"

# Copy entrypoint script
COPY dev/mcp/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8083

CMD ["/app/entrypoint.sh"]
