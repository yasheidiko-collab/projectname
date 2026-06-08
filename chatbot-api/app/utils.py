"""
Utility Functions
"""

import uuid
import hashlib
from datetime import datetime

def generate_request_id() -> str:
    """Generate unique request ID"""
    return str(uuid.uuid4())[:8]

def generate_session_id() -> str:
    """Generate session ID for conversation memory"""
    return str(uuid.uuid4())

def hash_user_input(text: str) -> str:
    """Hash user input for logging (privacy)"""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text for logging"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."