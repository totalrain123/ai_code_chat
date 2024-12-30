from .base_model import BaseAIModel
from typing import List, Optional
import json
import requests
import os

class HunyuanModel(BaseAIModel):
    def __init__(self):
        self.api_key = os.getenv('TENCENT_API_KEY')
        self.api_secret = os.getenv('TENCENT_API_SECRET')
        self.api_url = "https://hunyuan.cloud.tencent.com/hyllm/v1/chat/completions"
        
    async def preprocess(self, message: str) -> str:
        return message.strip()
        
    async def postprocess(self, response: str) -> str:
        return response.strip()
        
    async def generate_response(self, message: str, context: Optional[List] = None) -> str:
        message = await self.preprocess(message)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "stream": False
            }
            
            if context:
                payload["messages"] = context + payload["messages"]
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return await self.postprocess(result["choices"][0]["message"]["content"])
            
        except Exception as e:
            print(f"Hunyuan Model Error: {str(e)}")
            raise Exception("Failed to generate response") 