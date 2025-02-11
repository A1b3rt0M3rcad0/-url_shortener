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

        self.__validate_user_existence(username, user_repository)

        try:
            user_repository.delete(username)
        except Exception as e:
            message = f"Failed to delete user: {e}"
            raise HttpBadRequestError(message) from e

        return self.__format_response(username)

    @staticmethod
    def __validate_username(username:str) -> None:
        
        if not username.strip():
            raise HttpBadRequestError('The username cannot be empty or only spaces')

        if ' ' in username:
            raise HttpBadRequestError('The username cannot have empty spaces')
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise HttpBadRequestError('The username can only contain letters, numbers, underscores, and hyphens')
    
    def __validate_user_existence(self, username:str, user_repository:UsersRepositoryInterface) -> None:
        user = user_repository.select(username)
        if not user:
            raise HttpBadRequestError('User does not exist')
    
    @staticmethod
    def __format_response(username:str) -> Dict:
        response = {
            'type': 'Users',
            'count': 1,
            'attributes': {
                'username': username
            }
        }
        return response