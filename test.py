import torch
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import jsonschema
import json

json_schema = {
    "type": "object",
    "definitions": {
        "Region": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "population": {"type": "number"},
                "sub_regions": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Region"}
                }
            },
            "required": ["name"]
        },
        "Language": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "is_official": {"type": "boolean"},
                "dialects": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["name", "is_official"]
        },
        "CapitalCity": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "country": {"type": "string"},
                "population": {"type": "number"},
                "languages": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Language"}
                },
                "regions": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Region"}
                },
                "neighboring_cities": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/CapitalCity"}
                }
            },
            "required": ["name", "country"]
        }
    },
    "properties": {
        "answer": {"$ref": "#/definitions/CapitalCity"}
    },
    "required": ["answer"]
}

start_time = time.time()

model_name = "Qwen/Qwen3-14B"

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    ),
    AutoTokenizer.from_pretrained(model_name)
)

print("Generating with model: ", model_name)

output_type = outlines.types.JsonSchema(json_schema)
generator = outlines.Generator(model, output_type)

prompt = "what is the capital of Latvia, its population, and the languages spoken in the country?"

result = generator(prompt, max_new_tokens=1000)

print(result)

try:
    # print(output_type.validate_json(result.text))
    jsonschema.validate(json.loads(result.text), json_schema)
    print("✅ Result is valid against the schema")
except Exception as e:
    print(f"❌ Unexpected error during validation: {e}")

elapsed = time.time() - start_time
print("Time taken:", f"{elapsed:.2g}s")