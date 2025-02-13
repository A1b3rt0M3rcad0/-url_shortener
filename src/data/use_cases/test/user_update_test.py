from datetime import datetime, timezone
from sqlalchemy import text
from src.errors.types.bad_request import HttpBadRequestError
from src.errors.types.http_conflict import HttpConflictError
from src.data.use_cases.user_update import UserUpdate
from src.infra.db.repositories.users_repository import UsersRepository
from src.infra.db.test.connection import TDBConnectionHandler

database_connection = TDBConnectionHandler()
connection = database_connection.get_engine()

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

    return username

def get_user(username):
    sql = 'SELECT * FROM users WHERE username = :username'
    with connection.connect() as conn:
        response = conn.execute(text(sql), {"username": username})
        return response.one_or_none()

def cleanup(user_id, username):
    with connection.connect() as conn:
        conn.execute(text('DELETE FROM urls WHERE user_id = :user_id'), {"user_id": user_id})
        conn.execute(text('DELETE FROM users WHERE username = :username'), {"username": username})
        conn.commit()

def test_user_update():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    mocked_new_username = 'username2'

    insert_user(mocked_username, mocked_password, mocked_is_active, mocked_created_at)

    user_update = UserUpdate(UsersRepository, TDBConnectionHandler)
    user_update.update(mocked_username, {
        'username': mocked_new_username
    })
    user = get_user(mocked_new_username)
    cleanup(0, mocked_new_username)
    assert user.username == mocked_new_username

def test_update_validate_username():
    mocked_username = '  username'
    mocked_username2 = '   '
    mocked_username3 = 'username**@'

    user_update = UserUpdate(UsersRepository, TDBConnectionHandler)
    try:
        user_update.update(mocked_username, {'username': mocked_username})
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot have empty spaces'

    try:
        user_update.update(mocked_username2, {'username': mocked_username2})
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot be empty or only spaces'

    try:
        user_update.update(mocked_username3, {'username': mocked_username3})
    except HttpBadRequestError as e:
        assert e.message == 'The username can only contain letters, numbers, underscores, and hyphens'

def test_check_username_availability():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)

    insert_user(mocked_username, mocked_password, mocked_is_active, mocked_created_at)

    user_update = UserUpdate(UsersRepository, TDBConnectionHandler)

    try:
        user_update.update(mocked_username, {
            'username': mocked_username
        })
    except HttpConflictError as e:
        cleanup(0, mocked_username)
        assert e.message == 'A user with this name already exist'

def test_user_update_formate_response():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    mocked_password_2 = 'password2'

    insert_user(mocked_username, mocked_password, mocked_is_active, mocked_created_at)

    user_update = UserUpdate(UsersRepository, TDBConnectionHandler)
    response = user_update.update(mocked_username, {
        'password': mocked_password_2
    })
    cleanup(0, mocked_username)
    assert 'password' in response['attributes']['update_params'].keys()