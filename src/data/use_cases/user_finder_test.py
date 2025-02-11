from datetime import datetime, timezone
from sqlalchemy import text
from src.infra.db.test.connection import TDBConnectionHandler
from src.data.use_cases.user_finder import UserFinder
from src.infra.db.repositories.users_repository import UsersRepository
from src.errors.types.bad_request import HttpBadRequestError

database_connection = TDBConnectionHandler()
connection = database_connection.get_engine()

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

def test_user_finder_format_response():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    insert_user(mocked_username, mocked_password, mocked_is_active, mocked_created_at)
    user_finder = UserFinder(UsersRepository, TDBConnectionHandler)
    user = user_finder.finder(mocked_username)

    cleanup(0, mocked_username)
    assert user['attributes']['username'] == mocked_username
    assert user['attributes']['is_active'] == mocked_is_active
    assert user['attributes']['created_at'] == mocked_created_at

def test_register_validate_username():
    mocked_username = '  username'
    mocked_username2 = '   '
    mocked_username3 = 'username**@'

    user_finder = UserFinder(UsersRepository, TDBConnectionHandler)
    try:
        user_finder.finder(mocked_username)
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot have empty spaces'

    try:
        user_finder.finder(mocked_username2)
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot be empty or only spaces'

    try:
        user_finder.finder(mocked_username3)
    except HttpBadRequestError as e:
        assert e.message == 'The username can only contain letters, numbers, underscores, and hyphens'


def test_user_finder():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    insert_user(mocked_username, mocked_password, mocked_is_active, mocked_created_at)

    user_finder = UserFinder(UsersRepository, TDBConnectionHandler)
    user = user_finder.finder(mocked_username)
    cleanup(0, mocked_username)
    assert user