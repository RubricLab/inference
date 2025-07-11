FROM lmsysorg/sglang:latest

# Set environment variables
ENV HF_TOKEN=""
ENV SERVER_API_KEY=""
ENV PATH="/root/.bun/bin:$PATH"

# Install uv for faster Python dependency management
RUN pip install uv

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.18"

# Copy dependency files first for better layer caching
COPY auth/package.json auth/bun.lock auth/tsconfig.json ./
COPY pyproject.toml uv.lock ./

# Install Python dependencies with uv
RUN uv pip install sentencepiece --system

# Install Bun dependencies
RUN bun i --production

# Copy application code (after dependencies for better caching)
COPY auth/index.ts auth/env.ts ./

# Expose port
EXPOSE 3000

# Start services
CMD python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B \
    --host 0.0.0.0 \
    --port 8000 \
    --grammar-backend llguidance & \
    sleep 10 && \
    bun index.ts
