from datetime import datetime, timezone
from sqlalchemy import text
from src.data.use_cases.user_delete import UserDelete
from src.infra.db.repositories.users_repository import UsersRepository
from src.infra.db.test.connection import TDBConnectionHandler
from src.errors.types.bad_request import HttpBadRequestError

db_connection_handler = TDBConnectionHandler()
connection = db_connection_handler.get_engine()

def get_user(username):
    sql = 'SELECT * FROM users WHERE username = :username'
    with connection.connect() as conn:
        response = conn.execute(text(sql), {"username": username})
        return response.one_or_none()

def insert_user(username, password, is_active, created_at):
    sql = '''
    INSERT INTO users (username, password, is_active, created_at) 
    VALUES (:username, :password, :is_active, :created_at)
    '''
    with connection.connect() as conn:
        conn.execute(text(sql), {
            "username": username,
            "password": password,
            "is_active": is_active,
            "created_at": created_at
        })
        conn.commit()

    return get_user(username)

def cleanup(user_id, username):
    with connection.connect() as conn:
        conn.execute(text('DELETE FROM urls WHERE user_id = :user_id'), {"user_id": user_id})
        conn.execute(text('DELETE FROM users WHERE username = :username'), {"username": username})
        conn.commit()


def test_delete_response():

    mocked_username_1 = 'username'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    mocked_password = 'password'

    insert_user(mocked_username_1, mocked_password, mocked_is_active, mocked_created_at)

    users_delete = UserDelete(UsersRepository, TDBConnectionHandler)
    response = users_delete.delete(mocked_username_1)

    assert response['attributes']['username'] == mocked_username_1

def test_validate_username():
    mocked_username_1 = '  username'
    mocked_username_2 = '  '
    mocked_username_3 = '@username'

    users_delete = UserDelete(UsersRepository, TDBConnectionHandler)
    try:
        users_delete.delete(mocked_username_1)
        assert False
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot have empty spaces'
    
    try:
        users_delete.delete(mocked_username_2)
        assert False
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot be empty or only spaces'
    
    try:
        users_delete.delete(mocked_username_3)
        assert False
    except HttpBadRequestError as e:
        assert e.message == 'The username can only contain letters, numbers, underscores, and hyphens'

def test_non_existent_user():
    users_delete = UserDelete(UsersRepository, TDBConnectionHandler)
    try:
        users_delete.delete('non_existent_user')
    except HttpBadRequestError as e:
        assert e.message == 'User does not exist'
    
