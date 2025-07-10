FROM lmsysorg/sglang:latest

EXPOSE 8000

ENV HF_TOKEN=""
ENV SERVER_API_KEY=""

RUN pip install sentencepiece

CMD ["python", "-m", "sglang.launch_server", "--model-path", "Qwen/Qwen3-8B", "--host", "0.0.0.0", "--port", "8000", "--grammar-backend", "llguidance", "--api-key", "$SERVER_API_KEY"]