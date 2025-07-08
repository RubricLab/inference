FROM python:3.11.1-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /

COPY pyproject.toml uv.lock ./

# Set UV environment variables for faster builds
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=never

# Install with optimized flags
RUN uv sync --frozen --no-dev --no-install-project --no-build-isolation

COPY src/handler.py .

CMD ["uv", "run", "/handler.py"]