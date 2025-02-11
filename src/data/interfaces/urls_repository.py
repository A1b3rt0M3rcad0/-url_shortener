from typing import List, Dict
from abc import ABC, abstractmethod
from src.domain.models.urls import Urls

class UrlsRepositoryInterface(ABC):

    @abstractmethod
    def create(self, user_id:int, link:str, shortened_link:str) -> None:pass

    @abstractmethod
    def select(self, user_id: int) -> List[Urls]:pass

    @abstractmethod
    def delete(self, url_id:str) -> None:pass

    @abstractmethod
    def update(self, url_id:str, update_params:Dict) -> None:pass