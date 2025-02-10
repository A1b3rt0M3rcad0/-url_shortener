from datetime import datetime, timezone
import pytest
from sqlalchemy import text
from src.infra.db.settings.connection import DBConnectionHandler
from .users_repository import UsersRepository

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()

@pytest.mark.skip('Sensitive Test')
def test_create_user():

    mocked_username = 'username'
    mocked_password = 'password'

    users_repository = UsersRepository(DBConnectionHandler)
    users_repository.create(username=mocked_username, password=mocked_password)

    sql = f'''
    SELECT * FROM users
    WHERE username = '{mocked_username}'
    '''
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.username == mocked_username
    connection.execute(text(f'''
        DELETE FROM users WHERE username = {registry.username}
    '''))
    connection.commit()

@pytest.mark.skip(reason="Sensive test")
def test_select_user():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    sql = '''
        INSERT INTO users (username, password, is_active, created_at) VALUES ('{}', '{}', '{}', '{}')
    '''.format(mocked_username, mocked_password, mocked_is_active, mocked_created_at)
    connection.execute(text(sql))
    connection.commit()

    users_repository = UsersRepository(DBConnectionHandler)
    response = users_repository.select(mocked_username)
    user = response[0]

    assert user.username == mocked_username
    assert user.password == mocked_password
    assert user.is_active == mocked_is_active

    sql = f'''
    DELETE FROM users WHERE username = '{mocked_username}'
    '''
    connection.execute(text(sql))
    connection.commit()

@pytest.mark.skip(reason="Sensive test")
def test_delete_user():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    sql = '''
        INSERT INTO users (username, password, is_active, created_at) VALUES ('{}', '{}', '{}', '{}')
    '''.format(mocked_username, mocked_password, mocked_is_active, mocked_created_at)
    connection.execute(text(sql))
    connection.commit()

    users_repository = UsersRepository(DBConnectionHandler)
    users_repository.delete(mocked_username)

    sql = f'''
    SELECT * FROM users
    WHERE username = '{mocked_username}'
    '''
    response = connection.execute(text(sql))
    registrys = response.fetchall()

    assert len(registrys) == 0

    sql = f'''
    DELETE FROM users WHERE username = '{mocked_username}'
    '''
    connection.execute(text(sql))
    connection.commit()

@pytest.mark.skip(reason="Sensive test")
def test_update_user():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    sql = '''
        INSERT INTO users (username, password, is_active, created_at) VALUES ('{}', '{}', '{}', '{}')
    '''.format(mocked_username, mocked_password, mocked_is_active, mocked_created_at)
    connection.execute(text(sql))
    connection.commit()

    mocked_new_username = 'username2'

    users_repository = UsersRepository(DBConnectionHandler)
    users_repository.update(mocked_username, {'username': mocked_new_username})

    sql = f'''
    SELECT * FROM users
    WHERE username = '{mocked_new_username}'
    '''
    response = connection.execute(text(sql))
    registrys = response.fetchall()

    response = connection.execute(text(sql))
    registrys = response.fetchall()

    assert len(registrys) == 1

    sql = f'''
    DELETE FROM users WHERE username = '{mocked_new_username}'
    '''
    connection.execute(text(sql))
    connection.commit()
