from typing import Type
from abc import ABC, abstractmethod
from src.domain.interfaces.database_engine import DatabaseEngine

class DBConnectionHandlerInterface(ABC):

    @abstractmethod
    def get_engine(self) -> Type[DatabaseEngine]:pass
    
    @abstractmethod
    def __enter__(self):pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):pass