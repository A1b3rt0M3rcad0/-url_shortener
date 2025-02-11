import re
from typing import Dict
from src.domain.use_cases.user_register import UserRegister as UserRegisterInterface
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.domain.interfaces.connection import DBConnectionHandlerInterface
from src.errors.types.bad_request import HttpBadRequestError

class UserRegister(UserRegisterInterface):

    def __init__(self, 
                 user_repository:UsersRepositoryInterface,
                 database_connection:DBConnectionHandlerInterface
                 ) -> None:
        self.__user_repository = user_repository
        self.__database_connection = database_connection
    
    def register(self, username:str, password:str) -> Dict:
        self.__validate_username(username)
        self.__validate_password(password)
        user_repository = self.__user_repository(self.__database_connection)
        user_repository.create(username, password)
        response = self.__format_response(username)
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
    def __validate_password(password:str) -> None:

        if not password.strip():
            raise HttpBadRequestError('The password cannot be empty or only spaces')

        if ' ' in password:
            raise HttpBadRequestError('The password cannot have empty spaces')
    
    @staticmethod
    def __format_response(username:str) -> Dict:
        response = {
            "type": "Users",
            "count": 1,
            "attributes": {
                "username": username,
            }
        }
        return response