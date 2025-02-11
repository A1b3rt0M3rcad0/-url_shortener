#pylint:disable=C0103, R0902, W0611
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from src.domain.interfaces.connection import DBConnectionHandlerInterface
from src.infra.db.entities.url import Urls
from src.infra.db.entities.user import Users
from src.infra.db.settings.base import Base

class TDBConnectionHandler(DBConnectionHandlerInterface):

    def __init__(self) -> None:
        self.__connection_string = self.__create_connection_string()
        self.__engine = self.__create_engine()
        Base.metadata.create_all(self.__engine)
        self.session = None
    
    def __create_connection_string(self) -> str:
        return 'sqlite:///src/infra/db/test/test.db'
    
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