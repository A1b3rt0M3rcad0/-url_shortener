from typing import List, Dict
from abc import ABC, abstractmethod
from src.domain.models.users import Users

class UsersRepositoryInterface(ABC):

    @staticmethod
    @abstractmethod
    def create(username:str, password:str) -> None:pass

    @staticmethod
    @abstractmethod
    def select(username:str) -> List[Users]:pass

    @staticmethod
    @abstractmethod
    def delete(username:str) -> None:pass

    @staticmethod
    @abstractmethod
    def update(username:str, update_params:Dict) -> None:pass