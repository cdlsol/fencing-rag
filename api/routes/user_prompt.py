from fastapi import APIRouter, HTTPException
from api.models.user_prompt import Prompt
from api.services.rag import handle_rag_query
from api.utils.log import get_logger
from fastapi import APIRouter, HTTPException


log = get_logger(__name__)

router = APIRouter()

@router.post("/ask")
def ask_question(prompt: Prompt):
    log.info(f"Received question: {prompt.question}")
    try:
        result = handle_rag_query(prompt.question)
        log.info(f"Generated answer: {result['answer'][:100]}...")
        log.info(f"Context: {result['context'][:100]}...")
        return result
    except Exception as e:
        log.exception("Error occurred while handling RAG query.")
        raise HTTPException(status_code=500, detail=str(e))