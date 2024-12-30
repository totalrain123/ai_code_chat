from .base_model import BaseAIModel
from typing import List, Optional
import openai
import os

class GPTModel(BaseAIModel):
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    async def preprocess(self, message: str) -> str:
        # 在这里可以添加消息预处理逻辑
        return message.strip()
        
    async def postprocess(self, response: str) -> str:
        # 在这里可以添加响应后处理逻辑
        return response.strip()
        
    async def generate_response(self, message: str, context: Optional[List] = None) -> str:
        message = await self.preprocess(message)
        
        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": message})
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return await self.postprocess(result)
            
        except Exception as e:
            print(f"GPT Model Error: {str(e)}")
            raise Exception("Failed to generate response") 