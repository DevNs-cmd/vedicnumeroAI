from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(payload: ChatRequest, user=Depends(get_current_user)):
    user_msg = payload.message.lower()
    
    # Mock AI logic for numerology
    if "moolank" in user_msg or "root number" in user_msg:
        response = "Your Moolank (Root Number) is derived from your birth day. It defines your core personality. You can calculate yours in the Moolank section!"
    elif "bhagyank" in user_msg or "destiny" in user_msg:
        response = "Bhagyank is your Life Path Number, calculated from your full birth date (DD+MM+YYYY). It reveals your true purpose in this lifetime."
    elif "face" in user_msg or "reading" in user_msg:
        response = "Our AI Face Reading analyzes 68 landmarks on your face to reveal traits like intuition, courage, and wealth potential. Try uploading a photo in the Face Reading section!"
    elif "lucky" in user_msg:
        response = "Lucky numbers are influenced by your planetary vibrations. For most people, their Moolank and Bhagyank are their primary luck-bringers."
    elif "hello" in user_msg or "hi" in user_msg:
        response = "Namaste! I am your Cosmic Guide. How can I help you unlock your destiny today?"
    else:
        response = "The cosmos is vast! Could you please ask specifically about Moolank, Bhagyank, Face Reading, or Lucky Numbers? I'm here to guide your spiritual journey."

    return {"response": response}
