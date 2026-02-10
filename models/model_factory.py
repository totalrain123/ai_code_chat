import os
from typing import Dict, List, Optional, Type, TypedDict
from .base_model import BaseAIModel
from .hunyuan_model import HunyuanModel
from .qianwen_model import QianwenModel
from .wenxin_model import WenxinModel

class ModelConfig(TypedDict):
    name: str
    model_class: Type[BaseAIModel]
    required_env: List[str]

class ModelFactory:
    _models: Dict[str, ModelConfig] = {
        "hunyuan": {
            "name": "腾讯混元",
            "model_class": HunyuanModel,
            "required_env": ["TENCENT_API_KEY", "TENCENT_API_SECRET"]
        },
        "qianwen": {
            "name": "通义千问",
            "model_class": QianwenModel,
            "required_env": ["ALIBABA_API_KEY"]
        },
        "wenxin": {
            "name": "文心一言",
            "model_class": WenxinModel,
            "required_env": ["BAIDU_API_KEY", "BAIDU_SECRET_KEY"]
        }
    }

    _placeholder_prefixes = ("your_", "test_", "demo_")
    _placeholder_values = {"xxx", "changeme", "none", "null"}

    @classmethod
    def _is_effective_env_value(cls, value: Optional[str]) -> bool:
        if not value:
            return False

        normalized = value.strip()
        if not normalized:
            return False

        lowered = normalized.lower()
        if lowered in cls._placeholder_values:
            return False

        return not lowered.startswith(cls._placeholder_prefixes)

    @classmethod
    def _get_enabled_model_names(cls) -> List[str]:
        enabled_models = os.getenv("ENABLED_MODELS", "").strip()
        if not enabled_models:
            return list(cls._models.keys())

        enabled = []
        for model_name in enabled_models.split(","):
            normalized = model_name.strip()
            if normalized and normalized in cls._models and normalized not in enabled:
                enabled.append(normalized)
        return enabled

    @classmethod
    def get_missing_env_keys(cls, model_name: str) -> List[str]:
        if model_name not in cls._models:
            raise ValueError(f"Unsupported model: {model_name}")

        required_env = cls._models[model_name]["required_env"]
        return [
            env_key
            for env_key in required_env
            if not cls._is_effective_env_value(os.getenv(env_key))
        ]

    @classmethod
    def is_model_configured(cls, model_name: str) -> bool:
        return len(cls.get_missing_env_keys(model_name)) == 0

    @classmethod
    def get_default_model(cls) -> Optional[str]:
        enabled_models = cls._get_enabled_model_names()
        if not enabled_models:
            return None

        preferred_model = os.getenv("DEFAULT_MODEL", "").strip()
        if (
            preferred_model
            and preferred_model in enabled_models
            and cls.is_model_configured(preferred_model)
        ):
            return preferred_model

        for model_name in enabled_models:
            if cls.is_model_configured(model_name):
                return model_name

        return None

    @classmethod
    def get_model_options(cls) -> List[Dict[str, object]]:
        model_names = cls._get_enabled_model_names()
        options = []
        for model_name in model_names:
            missing_env = cls.get_missing_env_keys(model_name)
            model_meta = cls._models[model_name]
            options.append(
                {
                    "id": model_name,
                    "name": model_meta["name"],
                    "configured": len(missing_env) == 0,
                    "missing_env": missing_env
                }
            )
        return options

    @classmethod
    def get_model(cls, model_name: str) -> BaseAIModel:
        if model_name not in cls._models:
            raise ValueError(f"Unsupported model: {model_name}")

        if model_name not in cls._get_enabled_model_names():
            raise ValueError(f"Model is disabled: {model_name}")

        missing_env = cls.get_missing_env_keys(model_name)
        if missing_env:
            raise ValueError(
                f"Model is not configured: {model_name}. Missing env: {', '.join(missing_env)}"
            )

        model_class = cls._models[model_name]["model_class"]
        return model_class()