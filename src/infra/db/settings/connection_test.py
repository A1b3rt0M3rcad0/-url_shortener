#pylint:disable=missing-final-newline
import pytest
from sqlalchemy import inspect
from .connection import DBConnectionHandler

@pytest.mark.skip(reason="Sensive test")
def test_create_database_engine():
    db_connection_handle = DBConnectionHandler()
    engine = db_connection_handle.get_engine()
    connection = engine.connect()
    assert connection is not None
    inspector = inspect(engine)
    assert inspector.has_table('test')
    connection.close()