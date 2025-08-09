from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from init_ollama import wait_for_ollama
from contextlib import asynccontextmanager
from dto.code_generation import CodeGenerationRequest, CodeGenerationResponse
from agent import Agent
import logging
from typing import List
from pydantic import BaseModel

# Create documents directory if it doesn't exist
DOCUMENTS_DIR = Path("/app/documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI"""
    # Startup
    if not wait_for_ollama():
        raise Exception("Failed to initialize Ollama service")
    yield
    # Shutdown
    pass

app = FastAPI(title="Local Support Bot", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("api")

@app.get("/")
async def root():
    return {"message": "Local Support Bot API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to be processed and embedded
    """
    file_path = DOCUMENTS_DIR / file.filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"filename": file.filename, "status": "uploaded"}

class CodeGenerationResponse(BaseModel):
    code: str
    model: str

@app.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest = Body(...)):
    """
    Generate code for a given task using the Agent (LLM + RAG).
    """
    logger.info(f"Received code generation request: task='{request.task}'")
    if not request.task or not request.task.strip():
        logger.info("Empty task received, returning empty code response.")
        return CodeGenerationResponse(code="", model="")
    agent = Agent()
    code = agent.generate_code(task=request.task, context=request.context)
    logger.info("Code generation complete.")
    return CodeGenerationResponse(code=code, model="")

class CodeReviewRequest(BaseModel):
    code: str

class CodeReviewResponse(BaseModel):
    review: str
    model: str

class AgentHistoryItem(BaseModel):
    document: str
    metadata: dict

class AgentHistoryResponse(BaseModel):
    history: List[AgentHistoryItem]

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest = Body(...)):
    """
    Review code for quality, bugs, and improvements using the Agent.
    """
    logger.info("Received code review request.")
    try:
        agent = Agent()
        review = agent.review_code(code=request.code)
        logger.info("Code review complete.")
        return CodeReviewResponse(review=review, model="")
    except Exception as e:
        logger.error(f"Error during code review: {e}")
        raise HTTPException(status_code=500, detail="Code review failed.")

@app.get("/history", response_model=AgentHistoryResponse)
async def get_agent_history(limit: int = 10):
    """
    Retrieve recent agent history from vector DB.
    """
    logger.info(f"Fetching agent history, limit={limit}")
    try:
        agent = Agent()
        results = agent.get_history(limit=limit)
        # Format results for response
        history = [AgentHistoryItem(document=doc, metadata=meta)
                   for doc, meta in zip(results.get('documents', []), results.get('metadatas', []))]
        return AgentHistoryResponse(history=history)
    except Exception as e:
        logger.error(f"Error fetching agent history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch agent history.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
