FROM lmsysorg/sglang:latest

ENV HF_TOKEN=""
ENV SERVER_API_KEY=""

RUN curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.18"
ENV PATH="/root/.bun/bin:$PATH"

RUN pip install sentencepiece

COPY auth/package.json auth/index.ts ./

RUN bun i

EXPOSE 3000

CMD python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B \
    --host 0.0.0.0 \
    --port 8000 \
    --grammar-backend llguidance & \
    sleep 10 && \
    && ls \
    bun index.ts
