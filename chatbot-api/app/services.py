"""
AI Service - Groq Integration
"""

import time
import json
from typing import List, Dict, Any, Optional
from groq import Groq, APIError, RateLimitError, APIConnectionError

class AIService:
    """Service for interacting with Groq AI"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    def stream_response(self, messages: List[Dict], model: str, temperature: float, max_tokens: int):
        """Generator for streaming responses"""
        
        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except RateLimitError:
            yield {"error": "Rate limit exceeded. Please try again."}
        except APIConnectionError:
            yield {"error": "Network error. Check your connection."}
        except APIError as e:
            yield {"error": f"AI service error: {str(e)}"}
        except Exception as e:
            yield {"error": f"Unexpected error: {str(e)}"}
    
    def get_response(self, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict:
        """Get non-streaming response"""
        
        start_time = time.time()
        
        response = self.client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return {
            "id": response.id,
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "latency_ms": elapsed_ms,
            "created": response.created
        }

class SessionStore:
    """Store conversation history per session"""
    
    def __init__(self):
        self.sessions = {}
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get messages for session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": content})
        
        if len(self.sessions[session_id]) > 20:
            self.sessions[session_id] = self.sessions[session_id][-20:]
    
    def clear_session(self, session_id: str):
        """Clear session history"""
        if session_id in self.sessions:
            del self.sessions[session_id]

session_store = SessionStore()