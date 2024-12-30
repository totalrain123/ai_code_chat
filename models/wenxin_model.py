from .base_model import BaseAIModel
from typing import List, Optional
import requests
import os

class WenxinModel(BaseAIModel):
    def __init__(self):
        self.api_key = os.getenv('BAIDU_API_KEY')
        self.secret_key = os.getenv('BAIDU_SECRET_KEY')
        self.access_token = self._get_access_token()
        self.api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={self.access_token}"
        
    def _get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(url, params=params)
        return response.json().get("access_token")
        
    async def preprocess(self, message: str) -> str:
        return message.strip()
        
    async def postprocess(self, response: str) -> str:
        return response.strip()
        
    async def generate_response(self, message: str, context: Optional[List] = None) -> str:
        message = await self.preprocess(message)
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7
            }
            
            if context:
                payload["messages"] = context + payload["messages"]
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return await self.postprocess(result["result"])
            
        except Exception as e:
            print(f"Wenxin Model Error: {str(e)}")
            raise Exception("Failed to generate response") 