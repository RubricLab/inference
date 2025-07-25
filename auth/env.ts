import { createEnv } from "@t3-oss/env-core";
import { z } from "zod/v4";

export const env = createEnv({
	server: {
		SERVER_API_KEY: z.string().min(1),
	},
	clientPrefix: "",
	client: {},
	runtimeEnv: process.env,
});
