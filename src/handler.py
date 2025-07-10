import os
import runpod
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-14B"

hf_token = os.getenv("HF_TOKEN")

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(
        model_name,
        token=hf_token
    ),
    AutoTokenizer.from_pretrained(
        model_name,
        token=hf_token
    )
)

def handler(job):
    job_input = job["input"]
    prompt = job_input.get("prompt")
    schema = job_input.get("schema")
    
    if not job_input.get("schema", False):
        return {
            "error": "Input is missing the 'schema' key. Please include a schema."
        }
        
    print("Generating with model: ", model_name)
    
    output_type = outlines.types.JsonSchema(schema)
    generator = outlines.Generator(model, output_type)
    
    print("Prepped output type...")
    
    result = generator(prompt, max_new_tokens=500)
    
    print("Generated result...")
    
    return {"result": result}

if __name__ == '__main__':
    runpod.serverless.start({"handler": handler})