#pylint:disable=C0103, R0902
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine

load_dotenv()

class DBConnectionHandler:

    def __init__(self) -> None:

        self.DB_DATABASE = os.environ.get('DB_DATABASE')
        self.DB_DRIVER = os.environ.get('DB_DRIVER')
        self.DB_USERNAME = os.environ.get('DB_USERNAME')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_URL = os.environ.get('DB_URL')
        self.DB_PORT = os.environ.get('DB_PORT')
        self.DB_DB = os.environ.get('DB_DB')

        self.__connection_string = self.__create_connection_string()
        self.__engine = self.__create_engine()
        self.session = None
    
    def __create_connection_string(self) -> str:
        if all([self.DB_DATABASE, self.DB_DRIVER, self.DB_USERNAME, self.DB_PASSWORD, self.DB_URL, self.DB_PORT, self.DB_DB]):
            return f"{self.DB_DATABASE}+{self.DB_DRIVER}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_URL}:{self.DB_PORT}/{self.DB_DB}"
        raise ValueError("one or more environment variables could not be loaded")
    
    def __create_engine(self) -> Engine:
        return create_engine(self.__connection_string)
    
    def get_engine(self) -> Engine:
        return self.__engine
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()