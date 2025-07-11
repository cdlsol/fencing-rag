from fastapi import APIRouter, HTTPException
from api.models.user_prompt import Prompt
from api.services.rag import handle_rag_query
from api.utils.log import get_logger
from fastapi import APIRouter, HTTPException


log = get_logger(__name__)

router = APIRouter()

@router.post("/ask")
def ask_question(prompt: Prompt):
    try:
        return handle_rag_query(prompt.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))