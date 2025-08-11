from pydantic import BaseModel

class MCPContextRequest(BaseModel):
    context_type: str
    payload: dict

class MCPContextResponse(BaseModel):
    status: str
    data: dict

