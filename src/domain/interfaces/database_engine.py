from abc import ABC, abstractmethod
from typing import Any
class DatabaseEngine(ABC):
    
    @abstractmethod
    def connect(self) -> Any:
        """Método para conectar ao banco de dados"""

    @abstractmethod
    def dispose(self) -> None:
        """Método para limpar a conexão"""