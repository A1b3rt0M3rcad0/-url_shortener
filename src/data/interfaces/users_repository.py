from typing import List, Dict
from abc import ABC, abstractmethod
from src.domain.models.users import Users

class UsersRepositoryInterface(ABC):

    @abstractmethod
    def create(self, username:str, password:str) -> None:pass

    @abstractmethod
    def select(self, username:str) -> List[Users]:pass

    @abstractmethod
    def delete(self, username:str) -> None:pass

    @abstractmethod
    def update(self, username:str, update_params:Dict) -> None:pass