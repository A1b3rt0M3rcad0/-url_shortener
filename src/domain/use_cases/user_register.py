from abc import ABC, abstractmethod

class UserRegister(ABC):

    @abstractmethod
    def register(self, username:str, password:str) -> None:pass