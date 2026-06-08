# ChatBot API - Production Ready

A production-grade chatbot API powered by Groq, featuring streaming responses, rate limiting, and session memory.

## Features

✅ **Streaming Responses** - Real-time chat with SSE support  
✅ **Session Memory** - Maintain conversation context  
✅ **Rate Limiting** - 30 requests/minute per client  
✅ **Docker Support** - Easy deployment  
✅ **Multiple Models** - Llama 3.3, Llama 3.1, Mixtral  
✅ **Production Logging** - Request/response tracking  

## Quick Start

### Local Development

```bash
# Copy .env from example
cp chatbot-api/.env.example chatbot-api/.env

# Add your Groq API key
echo "GROQ_API_KEY=your-key-here" >> chatbot-api/.env

# Install dependencies
pip install -r chatbot-api/requirements.txt

# Run API
python main.py
```

API will be available at `http://localhost:8000`

### Docker

```bash
cd chatbot-api
docker-compose up
```

## API Endpoints

- **POST /v1/chat** - Send a message (streaming or non-streaming)
- **GET /v1/health** - Health check
- **GET /v1/metrics** - Usage statistics
- **POST /v1/session/clear** - Clear session history

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
python chatbot-api/test_api.py
```
