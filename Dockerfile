FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /

COPY pyproject.toml uv.lock ./

# Set UV environment variables for faster builds
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=never

# Install Python 3.11+ using uv and install dependencies
RUN uv python install 3.11 && \
    uv sync --frozen --no-dev --no-install-project --no-build-isolation

# Expose the port
EXPOSE 8000

# Set environment variable for HuggingFace token (will be overridden at runtime)
ENV HF_TOKEN=""

# Install sglang for the server functionality
RUN uv add sglang

# Use uv run to execute the sglang server
CMD ["uv", "run", "sglang.launch_server", "--model-path", "Qwen/Qwen3-8B", "--host", "0.0.0.0", "--port", "8000", "--grammar-backend", "llguidance"]