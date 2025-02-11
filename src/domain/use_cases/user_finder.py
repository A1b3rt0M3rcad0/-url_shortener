from abc import ABC, abstractmethod


class UserFinder(ABC):

    @abstractmethod
    def finder(self, username:str) -> None:pass