import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastapi import FastAPI, Request

app = FastAPI()

# json_schema = {
#     "type": "object",
#     "definitions": {
#         "Region": {
#             "type": "object",
#             "properties": {
#                 "name": {"type": "string"},
#                 "population": {"type": "number"},
#                 "sub_regions": {
#                     "type": "array",
#                     "items": {"$ref": "#/definitions/Region"}
#                 }
#             },
#             "required": ["name"]
#         },
#         "Language": {
#             "type": "object",
#             "properties": {
#                 "name": {"type": "string"},
#                 "is_official": {"type": "boolean"},
#                 "dialects": {
#                     "type": "array",
#                     "items": {"type": "string"}
#                 }
#             },
#             "required": ["name", "is_official"]
#         },
#         "CapitalCity": {
#             "type": "object",
#             "properties": {
#                 "name": {"type": "string"},
#                 "country": {"type": "string"},
#                 "population": {"type": "number"},
#                 "languages": {
#                     "type": "array",
#                     "items": {"$ref": "#/definitions/Language"}
#                 },
#                 "regions": {
#                     "type": "array",
#                     "items": {"$ref": "#/definitions/Region"}
#                 },
#                 "neighboring_cities": {
#                     "type": "array",
#                     "items": {"$ref": "#/definitions/CapitalCity"}
#                 }
#             },
#             "required": ["name", "country"]
#         }
#     },
#     "properties": {
#         "answer": {"$ref": "#/definitions/CapitalCity"}
#     },
#     "required": ["answer"]
# }
    
model_name = "microsoft/Phi-4-mini-instruct"

# result = generator("What's the capital of Latvia, its languages, and its rough population?", max_new_tokens=500)

# try:
#     print(output_type.validate(result))
#     print("✅ Result is valid against the schema")
# except Exception as e:
#     print(f"❌ Unexpected error during validation: {e}")
    
@app.post("/")
async def generate(request: Request):
    data = await request.json()
    
    if ("prompt" not in data):
        return {"error": "Prompt is required"}
    
    if ("schema" not in data):
        return {"error": "Schema is required"}
    
    model = outlines.from_transformers(
        AutoModelForCausalLM.from_pretrained(model_name),
        AutoTokenizer.from_pretrained(model_name)
    )

    output_type = outlines.types.JsonSchema(data["schema"])
    generator = outlines.Generator(model, output_type)
    
    result = generator(data["prompt"], max_new_tokens=500)
    
    return {"result": result}
    
@app.get("/")
    def handler(request: Request):
        return {"result":"try POST with a prompt and stringified JSON schema"}