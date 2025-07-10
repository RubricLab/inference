FROM lmsysorg/sglang:latest

EXPOSE 8000

ENV HF_TOKEN=""

RUN pip install sentencepiece

CMD ["python", "-m", "sglang.launch_server", "--model-path", "Qwen/Qwen3-8B", "--host", "0.0.0.0", "--port", "8000", "--grammar-backend", "llguidance"]