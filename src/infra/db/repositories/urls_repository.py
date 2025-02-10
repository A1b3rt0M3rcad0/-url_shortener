from typing import List, Dict
from src.domain.models.urls import Urls
from src.infra.db.entities.url import Urls as UrlsEntity
from src.data.interfaces.urls_repository import UrlsRepositoryInterface
from src.domain.interfaces.connection import DBConnectionHandlerInterface

class UrlsRepository(UrlsRepositoryInterface):

    def __init__(self, database_connection:DBConnectionHandlerInterface) -> None:
        self.__database_connection = database_connection
    
    def create(self, user_id:int, link:str, shortened_link:str) -> None:
        with self.__database_connection() as database:
            try:
                url = UrlsEntity(user_id=user_id, link=link, shortened_link=shortened_link)
                database.session.add(url)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
    
    def select(self, url_id:int) -> List[Urls]:
        with self.__database_connection() as database:
            try:
                urls = database.session.query(UrlsEntity)\
                .filter(UrlsEntity.id == url_id)\
                .all()
                return urls
            except Exception as exception:
                database.session.rollback()
                raise exception
    
    def delete(self, url_id:int) -> None:
        with self.__database_connection() as database:
            try:
                database.session.query(UrlsEntity)\
                    .filter(UrlsEntity.id == url_id)\
                    .delete()
                database.session.commit()
            except Exception as exception:
                database.rollback()
                raise exception
    
    def update(self, url_id:str, update_params:Dict) -> None:
        with self.__database_connection() as database:
            try:
                database.session.query(UrlsEntity)\
                    .filter(UrlsEntity.username == url_id)\
                    .update(update_params)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception