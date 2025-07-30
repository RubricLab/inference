import { Ajv } from "ajv";
import { OpenAI } from "openai";
import { env } from "./env";

const schemaValidator = new Ajv();

const openai = new OpenAI({
	apiKey: env.OPENAI_API_KEY,
	baseURL: env.OPENAI_BASE_URL,
});

console.log("OpenAI initialized with base URL:", openai.baseURL);

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

const MAX_TOKENS = 4000;

const response = await openai.chat.completions.create({
	model: "n/a",
	messages: [
		{
			role: "system",
			content:
				"You are a helpful assistant. Please first think then answer according to the provided JSON schema.",
		},
		{
			role: "user",
			content: "tell me about Latvia!",
		},
	],
	stream: true,
	max_tokens: MAX_TOKENS,
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
let reasoning = "";
for await (const chunk of response) {
	const part = chunk.choices[0]?.delta.content || "";
	result += part;
	const reasoningPart =
		(chunk.choices[0]?.delta as any).reasoning_content || "";
	reasoning += reasoningPart;
	process.stdout.write(reasoningPart);
}

const end = performance.now();

const CHARS_PER_TOKEN = 4;
const MS_PER_S = 1000;

try {
	const parsedResult = JSON.parse(result);
	const validate = schemaValidator.compile(schema);
	const isValid = validate(parsedResult);

	console.log(
		`\n${result.length + reasoning.length} tokens in ${~~(end - start)} ms (${~~(
			(((result.length + reasoning.length) / ~~(end - start)) * MS_PER_S) /
				CHARS_PER_TOKEN
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
