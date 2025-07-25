# Start with CUDA base image
ARG CUDA_VERSION=12.6.1
FROM nvidia/cuda:${CUDA_VERSION}-cudnn-devel-ubuntu22.04

# Set up env
ENV HF_TOKEN=""
ENV SERVER_API_KEY=""
ENV HF_HUB_ENABLE_HF_TRANSFER=1
ENV PYTHONPATH="/:/workspace"
ENV CUDA_HOME="/usr/local/cuda-12"
ENV LD_LIBRARY_PATH="/usr/local/cuda-12/lib64:$LD_LIBRARY_PATH"

# Add system deps
RUN apt update -y \
    && apt install -y --no-install-recommends curl unzip numactl ninja-build \
    && apt install -y python3.10-dev \
    && rm -rf /var/lib/apt/lists/*

# Add package managers
RUN (curl -fsSL https://astral.sh/uv/install.sh | sh) & (curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.18") & wait
ENV PATH="/root/.local/bin/:$PATH"
ENV PATH="/root/.bun/bin:$PATH"

# Copy source files
COPY auth/package.json auth/bun.lock auth/tsconfig.json auth/index.ts auth/env.ts ./
COPY pyproject.toml uv.lock ./

# Start virtual env
RUN uv venv .venv --python 3.10.12
ENV PATH=".venv/bin:$PATH"

# Install deps
RUN uv pip install sentencepiece
RUN uv pip install "sglang[all]>=0.4.9.post1" && uv pip install flashinfer-python -i https://flashinfer.ai/whl/cu126/torch2.6
RUN bun i -p

# Open web server port
EXPOSE 3000

# Start inference & web servers
CMD python -m sglang.launch_server \
    --model-path Qwen/Qwen3-30B-A3B-FP8 \
    --grammar-backend llguidance \
    --reasoning-parser qwen3 \
    --host 0.0.0.0 \
    --port 8000 & \
    bun index.ts
 