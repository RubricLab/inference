import { env } from './env'

const SGLANG_URL = 'http://localhost:8000'

const server = Bun.serve({
	async fetch(req) {
		const url = new URL(req.url)

		// Health check
		if (url.pathname === '/health') {
			return Response.json({ status: 'ok' })
		}

		// Only handle OpenAI endpoints
		if (!url.pathname.startsWith('/v1/')) {
			return new Response('Not Found', { status: 404 })
		}

		const auth = req.headers.get('authorization')
		if (!auth?.startsWith('Bearer ')) {
			return Response.json({ error: 'Unauthorized' }, { status: 401 })
		}

		try {
			const apiKey = auth.slice(7)
			if (apiKey !== env.SERVER_API_KEY) {
				return Response.json({ error: 'Unauthorized' }, { status: 401 })
			}

			// Forward to SGLang
			const response = await fetch(`${SGLANG_URL}${url.pathname}`, {
				body: req.method !== 'GET' ? await req.text() : null,
				headers: { 'content-type': 'application/json' },
				method: req.method
			})

			return new Response(response.body, {
				headers: response.headers,
				status: response.status
			})
		} catch (error) {
			console.error(error)
			return Response.json(
				{ details: JSON.stringify(error), error: 'Internal Server Error' },
				{ status: 500 }
			)
		}
	},
	port: process.env.PORT || 3000
})

console.log(`Auth server running on port ${server.port}`)
