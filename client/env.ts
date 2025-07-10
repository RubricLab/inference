import { createEnv } from "@t3-oss/env-core";
import { z } from "zod";

export const env = createEnv({
	server: {
		OPENAI_BASE_URL: z.url(),
		OPENAI_API_KEY: z.string().min(1),
	},
	clientPrefix: "",
	client: {},
	runtimeEnv: process.env,
});
