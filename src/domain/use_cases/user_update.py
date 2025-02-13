from abc import ABC, abstractmethod
from typing import Dict

class UserUpdate(ABC):

    @abstractmethod
    def update(self, username:str, update_params:Dict) -> None:pass