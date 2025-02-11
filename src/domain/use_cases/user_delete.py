from abc import ABC, abstractmethod

class UserDelete(ABC):

    @abstractmethod
    def delete(self, username:str) -> None:pass