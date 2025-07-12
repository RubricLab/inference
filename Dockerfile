ARG CUDA_VERSION=12.6.1
FROM nvidia/cuda:${CUDA_VERSION}-cudnn-devel-ubuntu22.04

ENV HF_TOKEN=""
ENV SERVER_API_KEY=""
ENV PYTHONPATH="/:/workspace"
ENV CUDA_HOME="/usr/local/cuda-12"
ENV LD_LIBRARY_PATH="/usr/local/cuda-12/lib64:$LD_LIBRARY_PATH"

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl unzip numactl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /bin/

RUN (curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.18") & wait

ENV PATH="/root/.bun/bin:$PATH"

COPY auth/package.json auth/bun.lock auth/tsconfig.json ./
COPY pyproject.toml uv.lock ./

RUN uv venv .venv --python 3.10.12
ENV PATH=".venv/bin:$PATH"

RUN uv pip install sentencepiece
RUN (uv pip install "sglang[all]>=0.4.9.post1" && uv pip install flashinfer-python -i https://flashinfer.ai/whl/cu126/torch2.6) & (bun i --production) & wait

COPY auth/index.ts auth/env.ts ./

EXPOSE 3000

CMD python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B \
    --host 0.0.0.0 \
    --port 8000 \
    --grammar-backend llguidance & \
    sleep 5 && \
    bun index.ts
