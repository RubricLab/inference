import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

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

model_name = "microsoft/Phi-4-mini-instruct"

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(model_name),
    AutoTokenizer.from_pretrained(model_name)
)

output_type = outlines.types.JsonSchema(json_schema)
generator = outlines.Generator(model, output_type)

prompt = "What's the capital of Latvia, its languages, and its rough population?"

result = generator(prompt, max_new_tokens=500)

try:
    print(output_type.validate(result))
    print("✅ Result is valid against the schema")
except Exception as e:
    print(f"❌ Unexpected error during validation: {e}")