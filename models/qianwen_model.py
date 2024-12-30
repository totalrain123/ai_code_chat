from .base_model import BaseAIModel
from typing import List, Optional
import dashscope
import os

class QianwenModel(BaseAIModel):
    def __init__(self):
        self.api_key = os.getenv('ALIBABA_API_KEY')
        dashscope.api_key = self.api_key
        
    async def preprocess(self, message: str) -> str:
        return message.strip()
        
    async def postprocess(self, response: str) -> str:
        return response.strip()
        
    async def generate_response(self, message: str, context: Optional[List] = None) -> str:
        message = await self.preprocess(message)
        
        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": message})
            
            response = dashscope.Generation.call(
                model='qwen-turbo',
                messages=messages,
                temperature=0.7,
                result_format='message'
            )
            
            if response.status_code == 200:
                return await self.postprocess(response.output.choices[0]['message']['content'])
            else:
                raise Exception(f"API Error: {response.code} - {response.message}")
            
        except Exception as e:
            print(f"Qianwen Model Error: {str(e)}")
            raise Exception("Failed to generate response") 