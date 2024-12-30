from typing import Dict, Type
from .base_model import BaseAIModel
from .hunyuan_model import HunyuanModel
from .qianwen_model import QianwenModel
from .wenxin_model import WenxinModel

class ModelFactory:
    _models: Dict[str, Type[BaseAIModel]] = {
        "hunyuan": HunyuanModel,
        "qianwen": QianwenModel,
        "wenxin": WenxinModel
    }
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseAIModel:
        if model_name not in cls._models:
            raise ValueError(f"Unsupported model: {model_name}")
        
        return cls._models[model_name]() 