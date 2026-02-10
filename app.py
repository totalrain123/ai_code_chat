from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn
from dotenv import load_dotenv
from models.model_factory import ModelFactory
from models.database import Database

load_dotenv()

app = FastAPI()
db = Database()

class ChatMessage(BaseModel):
    message: str
    model: Optional[str] = None
    context: Optional[list] = Field(default_factory=list)

class ConversationResponse(BaseModel):
    id: int
    user_message: str
    assistant_message: str
    model_name: str
    created_at: str

class ModelOptionResponse(BaseModel):
    id: str
    name: str
    configured: bool
    missing_env: List[str]

class ModelConfigResponse(BaseModel):
    default_model: Optional[str]
    models: List[ModelOptionResponse]

@app.get("/api/models", response_model=ModelConfigResponse)
async def get_models():
    try:
        return {
            "default_model": ModelFactory.get_default_model(),
            "models": ModelFactory.get_model_options()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(chat_message: ChatMessage):
    try:
        selected_model = chat_message.model or ModelFactory.get_default_model()
        if not selected_model:
            raise ValueError("No configured model available")

        model = ModelFactory.get_model(selected_model)
        response = await model.generate_response(
            message=chat_message.message,
            context=chat_message.context
        )
        
        # 保存对话到数据库
        await db.save_conversation(
            user_message=chat_message.message,
            assistant_message=response,
            model_name=selected_model
        )
        
        return {"message": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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