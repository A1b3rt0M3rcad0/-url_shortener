from typing import Dict
import re
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.domain.use_cases.user_delete import UserDelete as UserDeleteInterface
from src.domain.interfaces.connection import DBConnectionHandlerInterface
from src.errors.types.bad_request import HttpBadRequestError

class UserDelete(UserDeleteInterface):

    def __init__(self, 
                 user_repository:UsersRepositoryInterface,
                 database_connection:DBConnectionHandlerInterface
                 ) -> None:
        self.__user_repository = user_repository
        self.__database_connection = database_connection

    def delete(self, username:str) -> Dict:

        self.__validate_username(username)
        user_repository = self.__user_repository(self.__database_connection)

        if self.__check_if_the_user_exists(username, user_repository):
            user_repository.delete(username)
            return self.__format_response(username, success=True)
        return self.__format_response(username, success=False)
    
    @staticmethod
    def __validate_username(username:str) -> None:
        
        if not username.strip():
            raise HttpBadRequestError('The username cannot be empty or only spaces')

        if ' ' in username:
            raise HttpBadRequestError('The username cannot have empty spaces')
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise HttpBadRequestError('The username can only contain letters, numbers, underscores, and hyphens')
    
    def __check_if_the_user_exists(self, username:str, user_repository:UsersRepositoryInterface) -> bool:
        user = user_repository.select(username)
        return bool(user)
    
    @staticmethod
    def __format_response(username:str, success:bool) -> Dict:
        response = {
            'type': 'Users',
            'count': 1,
            'attributes': {
                'username': username
            },
            'success': success
        }
        return response