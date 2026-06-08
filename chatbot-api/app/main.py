"""
Production-Ready Chatbot API
Run: uvicorn app.main:app --reload
"""

import os
import json
import time
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import ChatRequest, ChatResponse, ErrorResponse, HealthResponse
from app.services import AIService, session_store
from app.middleware import LoggingMiddleware, rate_limiter, get_client_id
from app.utils import generate_request_id, format_timestamp

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    
    print("\n" + "="*60)
    print("🤖 PRODUCTION CHATBOT API")
    print("="*60)
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY not set in .env file")
        raise RuntimeError("Missing API key")
    
    app.state.ai_service = AIService(api_key=api_key)
    app.state.start_time = datetime.now()
    app.state.request_count = 0
    
    print("\n✅ Services initialized:")
    print(f"   • Groq AI: Ready")
    print(f"   • Rate Limiter: 30 requests/minute")
    print(f"   • Session Store: In-memory")
    
    print("\n📡 API Endpoints:")
    print("   POST /v1/chat      - Chat (streaming or non-streaming)")
    print("   GET  /v1/health    - Health check")
    print("   GET  /v1/metrics   - Usage metrics")
    print("   POST /v1/session/clear - Clear session")
    
    print("\n📚 Documentation:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    
    print("\n" + "="*60)
    print("✨ API ready! Waiting for requests...\n")
    
    yield
    
    print("\n" + "="*60)
    print("🛑 Shutting down...")
    print(f"📊 Total requests: {app.state.request_count}")
    print("👋 Goodbye!\n")

app = FastAPI(
    title="Production Chatbot API",
    description="Production-ready streaming chatbot API powered by Groq",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)