FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set environment variables
ENV HF_TOKEN=""
ENV SERVER_API_KEY=""
ENV PATH="/root/.bun/bin:$PATH"
ENV PYTHONPATH="/:/workspace"
ENV CUDA_HOME="/usr/local/cuda-12"

# Install system dependencies
RUN apt-get update -y \
    && apt-get install -y \
        python3-pip \
        python3-venv \
        curl \
        git \
        unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

RUN curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.18"

COPY auth/package.json auth/bun.lock auth/tsconfig.json ./auth/
COPY pyproject.toml uv.lock ./

# Install Python dependencies with uv
RUN uv pip install --system sentencepiece
RUN uv pip install --system flashinfer-python -i https://flashinfer.ai/whl/cu121/torch2.6
RUN uv pip install --system "sglang[all]>=0.4.9.post1" 

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
