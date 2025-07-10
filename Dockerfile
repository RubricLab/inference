FROM lmsysorg/sglang:latest

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /

COPY pyproject.toml uv.lock ./

# Set UV environment variables for faster builds
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=never

# Install with optimized flags and ensure Python is available
RUN uv sync --frozen --no-dev --no-install-project --no-build-isolation && \
    uv python install

# Expose the port
EXPOSE 8000

# Set environment variable for HuggingFace token (will be overridden at runtime)
ENV HF_TOKEN=""

# Use the same command as your current setup but with python3 -m for consistency
CMD ["uv", "run", "sglang.launch_server", "--model-path", "Qwen/Qwen3-8B", "--host", "0.0.0.0", "--port", "8000", "--grammar-backend", "llguidance"]