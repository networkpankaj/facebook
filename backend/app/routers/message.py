from fastapi import APIRouter
from app.models import Message
from app.database import db

router = APIRouter()

@router.post("/messages/")
async def send_message(message: Message):
    message_dict = message.dict()
    result = await db["messages"].insert_one(message_dict)
    return {"id": str(result.inserted_id)}

@router.get("/messages/{user_id}")
async def get_messages(user_id: str):
    messages = await db["messages"].find({"receiver_id": user_id}).to_list(length=100)
    return messages
