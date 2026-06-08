"""
Data Models for Chatbot API
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="user, assistant, or system")
    content: str = Field(..., description="Message content", min_length=1, max_length=10000)
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant', 'system']:
            raise ValueError('role must be user, assistant, or system')
        return v

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    session_id: Optional[str] = Field(None, description="Session ID for memory")
    model: str = Field("llama-3.3-70b-versatile", description="Model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Creativity")
    max_tokens: int = Field(500, ge=10, le=4000, description="Max response length")
    stream: bool = Field(True, description="Enable streaming")
    
    @validator('model')
    def validate_model(cls, v):
        allowed = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']
        if v not in allowed:
            raise ValueError(f'model must be one of {allowed}')
        return v

class ChatResponse(BaseModel):
    """Non-streaming response"""
    id: str
    content: str
    model: str
    session_id: Optional[str]
    usage: Dict[str, int]
    created: int

class ErrorResponse(BaseModel):
    """Error response format"""
    error: str
    detail: str
    timestamp: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime_seconds: float
    requests_processed: int