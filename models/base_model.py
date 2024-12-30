from abc import ABC, abstractmethod
from typing import List, Optional

class BaseAIModel(ABC):
    @abstractmethod
    async def generate_response(self, message: str, context: Optional[List] = None) -> str:
        pass
    
    @abstractmethod
    async def preprocess(self, message: str) -> str:
        pass
    
    @abstractmethod
    async def postprocess(self, response: str) -> str:
        pass 