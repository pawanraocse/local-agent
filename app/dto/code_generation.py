from pydantic import BaseModel
from typing import Optional, List, Dict

class CodeGenerationRequest(BaseModel):
    task: str
    context: str = ""

class CodeGenerationResponse(BaseModel):
    code: str
    model: Optional[str] = None
    error: Optional[str] = None
    trace: Optional[List[Dict]] = None
