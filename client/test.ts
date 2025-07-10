import Ajv from "ajv";
import { OpenAI } from "openai";

const ajv = new Ajv();

const openai = new OpenAI({
	apiKey: process.env.OPENAI_API_KEY,
	// baseURL: "https://llrrjy0uxucsfn-8000.proxy.runpod.net/v1",
	baseURL: "https://extended-jonell-rubric-1c426b40.koyeb.app/v1",
	// baseURL: "https://api.runpod.ai/v2/jbgbwpo385qb2n/openai/v1",
});

console.log("OpenAI initialized with base URL ", openai.baseURL);

const schema = {
	type: "object",
	additionalProperties: false,
	definitions: {
		Region: {
			type: "object",
			additionalProperties: false,
			properties: {
				name: { type: "string" },
				population: { type: "number" },
				sub_regions: {
					type: "array",
					items: { $ref: "#/definitions/Region" },
				},
			},
			required: ["name"],
		},
		Language: {
			type: "object",
			additionalProperties: false,
			properties: {
				name: { type: "string" },
				is_official: { type: "boolean" },
				dialects: {
					type: "array",
					items: { type: "string" },
				},
			},
			required: ["name", "is_official"],
		},
		CapitalCity: {
			type: "object",
			additionalProperties: false,
			properties: {
				name: { type: "string" },
				country: { type: "string" },
				population: { type: "number" },
				languages: {
					type: "array",
					items: { $ref: "#/definitions/Language" },
				},
				regions: {
					type: "array",
					items: { $ref: "#/definitions/Region" },
				},
				neighboring_cities: {
					type: "array",
					items: { $ref: "#/definitions/CapitalCity" },
				},
			},
			required: ["name", "country"],
		},
	},
	properties: {
		answer: { $ref: "#/definitions/CapitalCity" },
	},
	required: ["answer"],
};

const start = performance.now();

console.log("Starting...");

const response = await openai.chat.completions.create({
	// model: "meta-llama/Llama-3.1-8B",
	model: "Qwen/Qwen3-8B",
	messages: [
		{
			role: "system",
			content:
				"You are a helpful assistant. Please answer according to the provided JSON schema.",
		},
		{
			role: "user",
			content: "tell me about Toronto!",
			// "what is the capital of Latvia, its population, and the languages spoken in the country?",
		},
	],
	stream: true,
	max_tokens: 1000,
	temperature: 0.5,
	response_format: {
		type: "json_schema",
		json_schema: {
			name: "capital_city",
			schema,
		},
	},
});

let result = "";
for await (const chunk of response) {
	const part = chunk.choices[0]?.delta.content || "";
	result += part;
	process.stdout.write(part);
}

const end = performance.now();

try {
	const parsedResult = JSON.parse(result);
	const validate = ajv.compile(schema);
	const isValid = validate(parsedResult);

	console.log(
		`\n${result.length} tokens in ${~~(end - start)} ms (${~~(
			(result.length / ~~(end - start)) * 1000
		)} tokens/s)`,
	);

	if (isValid) {
		console.log("✅ Response is valid according to the JSON schema");
		console.dir({ parsedResult }, { depth: null });
	} else {
		console.log("❌ Response is invalid according to the JSON schema");
		console.log("Validation errors:", validate.errors);
		console.log("Raw result:", result);
	}
} catch (error) {
	console.log("❌ Failed to parse JSON response");
	console.log("Error:", error);
	console.log("Raw result:", result);
}
