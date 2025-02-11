import re
from typing import Dict, List
from datetime import datetime
from src.domain.models.users import Users
from src.domain.use_cases.user_finder import UserFinder as UserFinderInterface
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.domain.interfaces.connection import DBConnectionHandlerInterface
from src.errors.types.bad_request import HttpBadRequestError
from src.errors.types.http_not_found import HttpNotFoundError

class UserFinder(UserFinderInterface):

    def __init__(self, 
                 users_repository:UsersRepositoryInterface, 
                 database_connection:DBConnectionHandlerInterface
                 ) -> None:
        self.__users_repository = users_repository
        self.__database_connection = database_connection
    

    def finder(self, username:str) -> Dict:
        self.__validate_username(username)
        users_repository = self.__users_repository(self.__database_connection)
        users = users_repository.select(username)
        attributes = self.__collect_attributes(users)
        is_active = attributes['is_active']
        created_at = attributes['created_at']
        return self.__format_response(username, is_active, created_at)
    
    @staticmethod
    def __collect_attributes(users:List[Users]) -> Dict:
            
        if not users:
            raise HttpNotFoundError('User does not exist!')
            
        is_active = users[0].is_active
        created_at = users[0].created_at
        return {
            'is_active': is_active,
            'created_at': created_at
        }
    
    @staticmethod
    def __validate_username(username:str) -> None:
        
        if not username.strip():
            raise HttpBadRequestError('The username cannot be empty or only spaces')

        if ' ' in username:
            raise HttpBadRequestError('The username cannot have empty spaces')
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise HttpBadRequestError('The username can only contain letters, numbers, underscores, and hyphens')
    
    @staticmethod
    def __format_response(username:str, is_active:int, created_at:datetime) -> Dict:
        response = {
            "type": "Users",
            "count": 1,
            "attributes": {
                "username": username,
                "is_active": is_active,
                "created_at": created_at
            }
        }
        return response