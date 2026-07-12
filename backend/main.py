from fastapi import FastAPI, HTTPException
from models.schemas import ChatRequest, ChatResponse
from agents.router import route_question
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NexusAI API")


@app.get("/")
def health_check():
    
    return {"status": "NexusAI is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    
    logger.info(f"[API] Received question: {request.question}")

    try:
        result = route_question(request.question)
        return ChatResponse(
            question=result["question"],
            source_used=result["source_used"],
            answer=result["answer"]
        )
    except Exception as e:
        logger.error(f"[API] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))