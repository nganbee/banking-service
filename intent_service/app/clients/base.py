from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional

class BaseModelClient(ABC):
    
    @abstractmethod
    def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        **kwargs: Any
    ) -> str:
        pass

    @abstractmethod
    def chat(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        **kwargs: Any
    ) -> str:
        pass