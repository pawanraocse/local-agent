from pydantic import BaseModel

class CodeGenerationRequest(BaseModel):
    task: str
    context: str = ""

class CodeGenerationResponse(BaseModel):
    code: str

