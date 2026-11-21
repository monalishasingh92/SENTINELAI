from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.rag.rag_pipeline import ask_safety_assistant

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/api/assistant/chat")
async def chat_with_assistant(request: ChatRequest):

    try:
        result = ask_safety_assistant(request.question)

        return {
            "status": "success",
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Assistant error: {str(error)}"
        )