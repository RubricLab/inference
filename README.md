# Rubric Inference Stack

A minimalist open-source LLM inference stack with structured outputs using SGLang and minimal API key auth via a Bun web server for 3x higher throughput than FastAPI.

The stack is currently highly-opinionated and likely to generalize and change.

## Quickstart

The following assumes you're running on a Linux machine (likely in the cloud) with a GPU.

### Docker
```bash
docker build -t inference .
docker run -p 3000:3000 -p 8000:8000 \
  -e SERVER_API_KEY=your_api_key \
  -e HF_TOKEN=your_hf_token \
  inference
```

### Skypilot

Install [Skypilot](https://docs.skypilot.co/en/latest/getting-started/installation.html#installation) and connect an infra provider. We recommend using [uv](https://docs.astral.sh/uv/) for fast setup and [Vast](https://cloud.vast.ai/?ref_id=278361) for competitively-priced GPUs or [Runpod](https://runpod.io?ref=n92vmj04) for a good experience.

First, grab an API key from your cloud provider (e.g. [Vast](https://cloud.vast.ai/manage-keys) or [Runpod](https://console.runpod.io/user/settings)).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.10
source .venv/bin/activate
uv pip install "skypilot[vast,runpod]"

# Vast
uv pip install "vastai-sdk>=0.1.12"
echo "<your_vast_api_key>" > ~/.vast_api_key

# Runpod
uv pip install "runpod>=1.6.1"
runpod config # then enter your API key

sky launch skypilot.yaml
```

## Client Example

Test the API from any OpenAI-compatible client:

```bash
cd test && bun i && touch .env
```

Populate your **.env** with:
```
BASE_URL=http://localhost:3000/v1
SERVER_API_KEY=your_api_key
```

Run the test:
```bash
bun index.ts
```

You should see a reasoning chain and a JSON payload conforming to the schema.