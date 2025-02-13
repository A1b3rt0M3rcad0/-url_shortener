import re
from typing import Dict
from src.errors.types.bad_request import HttpBadRequestError
from src.errors.types.http_conflict import HttpConflictError
from src.domain.use_cases.user_update import UserUpdate as UserUpdateInterface
from src.domain.interfaces.connection import DBConnectionHandlerInterface
from src.data.interfaces.users_repository import UsersRepositoryInterface

class UserUpdate(UserUpdateInterface):
    
    def __init__(self, 
                 user_repository:UsersRepositoryInterface,
                 database_connetion:DBConnectionHandlerInterface
                 )->None:
        self.__user_repository = user_repository
        self.__database_connection = database_connetion
    
    def update(self, username:str, update_params:Dict) -> Dict:
        self.__validate_username(username)
        user_repository = self.__user_repository(self.__database_connection)
        self.__check_username_availability(user_repository, update_params)
        user_repository.update(username, update_params)
        response = self.__format_response(username, update_params)
        return response

    @staticmethod
    def __validate_username(username:str) -> None:
        
        if not username.strip():
            raise HttpBadRequestError('The username cannot be empty or only spaces')

        if ' ' in username:
            raise HttpBadRequestError('The username cannot have empty spaces')
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise HttpBadRequestError('The username can only contain letters, numbers, underscores, and hyphens')
    
    @staticmethod
    def __check_username_availability(user_repository:UsersRepositoryInterface, update_params:Dict) -> None:
        if 'username' in update_params:
            users = user_repository.select(update_params['username'])
            if users:
                raise HttpConflictError('A user with this name already exist')


    @staticmethod
    def __format_response(username:str, update_params:Dict) -> Dict:
        response = {
            "type": "Users",
            "count": 1,
            "attributes": {
                "username": username,
                "update_params": update_params
            }
        }
        return response