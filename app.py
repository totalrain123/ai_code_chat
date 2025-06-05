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

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ''

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
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


@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    try:
        task_id = await db.create_task(task.title, task.description)
        new_task = await db.get_task(task_id)
        return {
            "id": new_task[0],
            "title": new_task[1],
            "description": new_task[2],
            "status": new_task[3],
            "created_at": new_task[4]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks():
    try:
        tasks = await db.get_tasks()
        return [
            {
                "id": t[0],
                "title": t[1],
                "description": t[2],
                "status": t[3],
                "created_at": t[4]
            }
            for t in tasks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, status: str):
    try:
        updated = await db.update_task_status(task_id, status)
        return {
            "id": updated[0],
            "title": updated[1],
            "description": updated[2],
            "status": updated[3],
            "created_at": updated[4]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 