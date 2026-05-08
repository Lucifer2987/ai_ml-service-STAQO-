from fastapi import APIRouter
from app.models.schemas import ChatInput, ChatResponse
from app.services.chat_service import get_chat_response

router = APIRouter(prefix="/api/v1/chatbot", tags=["Chatbot"])

@router.post("/query", response_model=ChatResponse)
async def chatbot_query(body: ChatInput):
    result = get_chat_response(body.question, body.session_id)
    return ChatResponse(**result)