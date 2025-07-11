import { env } from './env'

const SGLANG_URL = 'http://localhost:8000'

const server = Bun.serve({
	port: process.env.PORT || 3000,
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
				method: req.method,
				headers: { 'content-type': 'application/json' },
				body: req.method !== 'GET' ? await req.text() : null
			})

			return new Response(response.body, {
				status: response.status,
				headers: response.headers
			})
		} catch (error) {
			console.error(error)
			return Response.json(
				{ error: 'Internal Server Error', details: JSON.stringify(error) },
				{ status: 500 }
			)
		}
	}
})

console.log(`Auth server running on port ${server.port}`)
