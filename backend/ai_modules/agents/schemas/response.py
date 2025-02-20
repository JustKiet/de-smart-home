from pydantic import BaseModel
from typing import Optional, Literal, List, Dict, Any, Callable

class OpenAIResponse(BaseModel):
    """Response schema for OpenAI."""
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    refusal: Optional[str] = None
    audio: Optional[str] = None