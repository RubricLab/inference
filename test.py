import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import jsonschema
import json

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
json_schema = {"type":"object","properties":{"chain":{"anyOf":[{"$ref":"#/$defs/abs"},{"$ref":"#/$defs/ceil"},{"$ref":"#/$defs/cos"},{"$ref":"#/$defs/degreesToRadians"},{"$ref":"#/$defs/divide"},{"$ref":"#/$defs/factorial"},{"$ref":"#/$defs/floor"},{"$ref":"#/$defs/getE"},{"$ref":"#/$defs/getPi"},{"$ref":"#/$defs/log"},{"$ref":"#/$defs/log10"},{"$ref":"#/$defs/modulo"},{"$ref":"#/$defs/multiply"},{"$ref":"#/$defs/negate"},{"$ref":"#/$defs/parse"},{"$ref":"#/$defs/power"},{"$ref":"#/$defs/radiansToDegrees"},{"$ref":"#/$defs/round"},{"$ref":"#/$defs/sin"},{"$ref":"#/$defs/sqrt"},{"$ref":"#/$defs/stringify"},{"$ref":"#/$defs/subtract"},{"$ref":"#/$defs/sum"},{"$ref":"#/$defs/tan"}]}},"required":["chain"],"additionalProperties":"false","$defs":{"abs":{"type":"object","properties":{"node":{"type":"string","const":"abs"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"number":{"anyOf":[{"$ref":"#/$defs/abs"},{"$ref":"#/$defs/ceil"},{"$ref":"#/$defs/cos"},{"$ref":"#/$defs/degreesToRadians"},{"$ref":"#/$defs/divide"},{"$ref":"#/$defs/factorial"},{"$ref":"#/$defs/floor"},{"$ref":"#/$defs/getE"},{"$ref":"#/$defs/getPi"},{"$ref":"#/$defs/log"},{"$ref":"#/$defs/log10"},{"$ref":"#/$defs/modulo"},{"$ref":"#/$defs/multiply"},{"$ref":"#/$defs/negate"},{"$ref":"#/$defs/parse"},{"$ref":"#/$defs/power"},{"$ref":"#/$defs/radiansToDegrees"},{"$ref":"#/$defs/round"},{"$ref":"#/$defs/sin"},{"$ref":"#/$defs/sqrt"},{"$ref":"#/$defs/subtract"},{"$ref":"#/$defs/sum"},{"$ref":"#/$defs/tan"},{"type":"number"}]},"ceil":{"type":"object","properties":{"node":{"type":"string","const":"ceil"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"cos":{"type":"object","properties":{"node":{"type":"string","const":"cos"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"degreesToRadians":{"type":"object","properties":{"node":{"type":"string","const":"degreesToRadians"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"divide":{"type":"object","properties":{"node":{"type":"string","const":"divide"},"input":{"$ref":"#/$defs/object(dividend:number,divisor:number)"}},"required":["node","input"],"additionalProperties":"false"},"object(dividend:number,divisor:number)":{"anyOf":[{"type":"object","properties":{"dividend":{"$ref":"#/$defs/number"},"divisor":{"$ref":"#/$defs/number"}},"required":["dividend","divisor"],"additionalProperties":"false"},{"type":"object","properties":{"dividend":{"type":"number"},"divisor":{"type":"number"}},"required":["dividend","divisor"],"additionalProperties":"false"}]},"factorial":{"type":"object","properties":{"node":{"type":"string","const":"factorial"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"floor":{"type":"object","properties":{"node":{"type":"string","const":"floor"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"getE":{"type":"object","properties":{"node":{"type":"string","const":"getE"},"input":{"$ref":"#/$defs/null"}},"required":["node","input"],"additionalProperties":"false"},"null":{"type":"null"},"getPi":{"type":"object","properties":{"node":{"type":"string","const":"getPi"},"input":{"$ref":"#/$defs/null"}},"required":["node","input"],"additionalProperties":"false"},"log":{"type":"object","properties":{"node":{"type":"string","const":"log"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"log10":{"type":"object","properties":{"node":{"type":"string","const":"log10"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"modulo":{"type":"object","properties":{"node":{"type":"string","const":"modulo"},"input":{"$ref":"#/$defs/object(dividend:number,divisor:number)"}},"required":["node","input"],"additionalProperties":"false"},"multiply":{"type":"object","properties":{"node":{"type":"string","const":"multiply"},"input":{"$ref":"#/$defs/object(multiplicand:number,multiplier:number)"}},"required":["node","input"],"additionalProperties":"false"},"object(multiplicand:number,multiplier:number)":{"anyOf":[{"type":"object","properties":{"multiplicand":{"$ref":"#/$defs/number"},"multiplier":{"$ref":"#/$defs/number"}},"required":["multiplicand","multiplier"],"additionalProperties":"false"},{"type":"object","properties":{"multiplicand":{"type":"number"},"multiplier":{"type":"number"}},"required":["multiplicand","multiplier"],"additionalProperties":"false"}]},"negate":{"type":"object","properties":{"node":{"type":"string","const":"negate"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"parse":{"type":"object","properties":{"node":{"type":"string","const":"parse"},"input":{"$ref":"#/$defs/string"}},"required":["node","input"],"additionalProperties":"false"},"string":{"anyOf":[{"$ref":"#/$defs/stringify"},{"type":"string"}]},"stringify":{"type":"object","properties":{"node":{"type":"string","const":"stringify"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"power":{"type":"object","properties":{"node":{"type":"string","const":"power"},"input":{"$ref":"#/$defs/object(base:number,exponent:number)"}},"required":["node","input"],"additionalProperties":"false"},"object(base:number,exponent:number)":{"anyOf":[{"type":"object","properties":{"base":{"$ref":"#/$defs/number"},"exponent":{"$ref":"#/$defs/number"}},"required":["base","exponent"],"additionalProperties":"false"},{"type":"object","properties":{"base":{"type":"number"},"exponent":{"type":"number"}},"required":["base","exponent"],"additionalProperties":"false"}]},"radiansToDegrees":{"type":"object","properties":{"node":{"type":"string","const":"radiansToDegrees"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"round":{"type":"object","properties":{"node":{"type":"string","const":"round"},"input":{"$ref":"#/$defs/object(decimals:union(number,null),value:number)"}},"required":["node","input"],"additionalProperties":"false"},"object(decimals:union(number,null),value:number)":{"anyOf":[{"type":"object","properties":{"decimals":{"$ref":"#/$defs/union(number,null)"},"value":{"$ref":"#/$defs/number"}},"required":["decimals","value"],"additionalProperties":"false"},{"type":"object","properties":{"decimals":{"anyOf":[{"type":"number"},{"type":"null"}]},"value":{"type":"number"}},"required":["decimals","value"],"additionalProperties":"false"}]},"union(number,null)":{"anyOf":[{"anyOf":[{"$ref":"#/$defs/number"},{"$ref":"#/$defs/null"}]},{"anyOf":[{"type":"number"},{"type":"null"}]}]},"sin":{"type":"object","properties":{"node":{"type":"string","const":"sin"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"sqrt":{"type":"object","properties":{"node":{"type":"string","const":"sqrt"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"},"subtract":{"type":"object","properties":{"node":{"type":"string","const":"subtract"},"input":{"$ref":"#/$defs/object(minuend:number,subtrahend:number)"}},"required":["node","input"],"additionalProperties":"false"},"object(minuend:number,subtrahend:number)":{"anyOf":[{"type":"object","properties":{"minuend":{"$ref":"#/$defs/number"},"subtrahend":{"$ref":"#/$defs/number"}},"required":["minuend","subtrahend"],"additionalProperties":"false"},{"type":"object","properties":{"minuend":{"type":"number"},"subtrahend":{"type":"number"}},"required":["minuend","subtrahend"],"additionalProperties":"false"}]},"sum":{"type":"object","properties":{"node":{"type":"string","const":"sum"},"input":{"$ref":"#/$defs/array(number)"}},"required":["node","input"],"additionalProperties":"false"},"array(number)":{"anyOf":[{"type":"array","items":{"$ref":"#/$defs/number"}},{"type":"array","items":{"type":"number"}}]},"tan":{"type":"object","properties":{"node":{"type":"string","const":"tan"},"input":{"$ref":"#/$defs/number"}},"required":["node","input"],"additionalProperties":"false"}}}

start_time = time.time()

model_name = "osmosis-ai/Osmosis-Structure-0.6B"
# model_name = "microsoft/Phi-4-mini-instruct"

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(model_name),
    AutoTokenizer.from_pretrained(model_name)
)

print("Generating with model: ", model_name)

output_type = outlines.types.JsonSchema(json_schema)
generator = outlines.Generator(model, output_type)

prompt = "how do we calculate 1+1 using the calculator tool? chain the operations to get it done"

result = generator(prompt, max_new_tokens=2000, temperature=0.5)

print(result)

try:
    # print(output_type.validate_json(result.text))
    jsonschema.validate(json.loads(result.text), json_schema)
    print("✅ Result is valid against the schema")
    elapsed = time.time() - start_time
    print("Time taken:", f"{elapsed:.2g}s")
except Exception as e:
    print(f"❌ Unexpected error during validation: {e}")