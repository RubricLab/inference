import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastapi import FastAPI, Request

app = FastAPI()

model_name = "microsoft/Phi-4-mini-instruct"
    
@app.post("/")
async def generate(request: Request):
    data = await request.json()
    
    if ("prompt" not in data):
        return {"error": "Prompt is required"}
    
    if ("schema" not in data):
        return {"error": "Schema is required"}
    
    print("Generating for schema:")
    print(data["schema"])
    
    model = outlines.from_transformers(
        AutoModelForCausalLM.from_pretrained(model_name),
        AutoTokenizer.from_pretrained(model_name)
    )
    
    print("Prepped model...")

    output_type = outlines.types.JsonSchema(data["schema"])
    generator = outlines.Generator(model, output_type)
    
    print("Prepped output type...")
    
    result = generator(data["prompt"], max_new_tokens=500)
    
    print("Generated result...")
    
    return {"result": result}
    
@app.get("/")
def handler(request: Request):
    return {"result":"try POST with a prompt and stringified JSON schema"}
