from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from models.model_factory import ModelFactory
from models.database import Database
from datetime import datetime

app = FastAPI()
db = Database()

class ChatMessage(BaseModel):
    message: str
    model: str
    context: Optional[list] = []

class ConversationResponse(BaseModel):
    id: int
    user_message: str
    assistant_message: str
    model_name: str
    created_at: str

@app.post("/api/chat")
async def chat(chat_message: ChatMessage):
    try:
        model = ModelFactory.get_model(chat_message.model)
        response = await model.generate_response(
            message=chat_message.message,
            context=chat_message.context
        )
        
        # 保存对话到数据库
        await db.save_conversation(
            user_message=chat_message.message,
            assistant_message=response,
            model_name=chat_message.model
        )
        
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations(limit: int = 100):
    try:
        conversations = await db.get_conversations(limit)
        return [
            {
                "id": conv[0],
                "user_message": conv[1],
                "assistant_message": conv[2],
                "model_name": conv[3],
                "created_at": conv[4]
            }
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 