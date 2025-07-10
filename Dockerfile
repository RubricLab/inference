FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /

COPY pyproject.toml uv.lock ./

# Set UV environment variables for faster builds
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=never

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project --no-build-isolation

# Expose the port
EXPOSE 8000

# Set environment variable for HuggingFace token (will be overridden at runtime)
ENV HF_TOKEN=""

# Install sglang for the server functionality
RUN uv pip install flashinfer-python -i https://flashinfer.ai/whl/cu126/torch2.6
RUN uv pip install "sglang[all]>=0.4.9.post1"

# Use uv run to execute the sglang server
CMD ["uv", "run", "sglang.launch_server", "--model-path", "Qwen/Qwen3-8B", "--host", "0.0.0.0", "--port", "8000", "--grammar-backend", "llguidance"]