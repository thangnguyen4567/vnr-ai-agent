from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    success: bool = Field(..., description="Success or failure of the request")
    message: str = Field(..., description="Message response")
    data: Optional[Any] = Field(None, description="Data response")

