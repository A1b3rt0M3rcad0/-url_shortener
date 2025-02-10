from typing import List, Dict
from src.infra.db.entities.user import Users as UsersEntity
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.domain.models.users import Users
from src.domain.interfaces.connection import DBConnectionHandlerInterface


class UsersRepository(UsersRepositoryInterface):

    def __init__(self, database_connection:DBConnectionHandlerInterface) -> None:
        self.__database_connection = database_connection
    
    def create(self, username:str, password:str) -> None:
        with self.__database_connection() as database:
            try:
                new_user = UsersEntity(username=username, password=password)
                database.session.add(new_user)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
    
    def select(self, username:str) -> List[Users]:
        with self.__database_connection() as database:
            try:
                users = database.session.query(UsersEntity)\
                    .filter(UsersEntity.username == username)\
                    .all()
                return users
            except Exception as exeception:
                raise exeception
    
    def delete(self, username:str) -> None:
        with self.__database_connection() as database:
            try:
                database.session.query(UsersEntity)\
                .filter(UsersEntity.username == username)\
                .delete()
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
    
    def update(self, username:str, update_params:Dict) -> None:
        with self.__database_connection() as database:
            try:
                database.session.query(UsersEntity)\
                    .filter(UsersEntity.username == username)\
                    .update(update_params)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception