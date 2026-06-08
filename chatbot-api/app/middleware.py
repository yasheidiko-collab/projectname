"""
Middleware - Logging, Rate Limiting, CORS
"""

import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict
from collections import defaultdict
from datetime import datetime

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def check_rate_limit(self, client_id: str) -> bool:
        """Check if client is within rate limit"""
        now = time.time()
        window_start = now - self.window_seconds
        
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        window_start = now - self.window_seconds
        recent = [t for t in self.requests[client_id] if t > window_start]
        return max(0, self.max_requests - len(recent))

rate_limiter = RateLimiter(max_requests=30, window_seconds=60)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", "unknown")
        start_time = time.time()
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📨 {request_id} | {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 {request_id} | {response.status_code} | {duration_ms:.0f}ms")
            return response
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {request_id} | ERROR | {duration_ms:.0f}ms | {str(e)}")
            raise

def get_client_id(request: Request) -> str:
    """Get client ID from request (IP or API key)"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"