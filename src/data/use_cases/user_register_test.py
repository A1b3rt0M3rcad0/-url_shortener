from sqlalchemy import text
from src.data.use_cases.user_register import UserRegister
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

def cleanup(user_id, username):
    with connection.connect() as conn:
        conn.execute(text('DELETE FROM urls WHERE user_id = :user_id'), {"user_id": user_id})
        conn.execute(text('DELETE FROM users WHERE username = :username'), {"username": username})
        conn.commit()

def test_register_format_response():

    mocked_username = 'username'
    mocked_password = 'password'

    user_register = UserRegister(UsersRepository, TDBConnectionHandler)
    response = user_register.register(mocked_username, mocked_password)

    assert response['attributes']['username'] == mocked_username
    assert response['type'] == 'Users'
    assert response['count'] == 1

    cleanup(0, mocked_username)

def test_register_validate_username():
    mocked_username = '  username'
    mocked_username2 = '   '
    mocked_username3 = 'username**@'
    mocked_password = 'password'

    user_register = UserRegister(UsersRepository, TDBConnectionHandler)
    try:
        user_register.register(mocked_username, mocked_password)
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot have empty spaces'

    try:
        user_register.register(mocked_username2, mocked_password)
    except HttpBadRequestError as e:
        assert e.message == 'The username cannot be empty or only spaces'

    try:
        user_register.register(mocked_username3, mocked_password)
    except HttpBadRequestError as e:
        assert e.message == 'The username can only contain letters, numbers, underscores, and hyphens'

def test_register_validade_password():
    mocked_username = 'username'
    mocked_password1 = '  password'
    mocked_password2 = '    '

    user_register = UserRegister(UsersRepository, TDBConnectionHandler)

    try:
        user_register.register(mocked_username, mocked_password1)
    except HttpBadRequestError as e:
        assert e.message == 'The password cannot have empty spaces'

    try:
        user_register.register(mocked_username, mocked_password2)
    except HttpBadRequestError as e:
        assert e.message == 'The password cannot be empty or only spaces'

def test_register():
    mocked_username = 'username'
    mocked_password = 'password'
    user_register = UserRegister(UsersRepository, TDBConnectionHandler)
    user_register.register(mocked_username, mocked_password)
    user = get_user(mocked_username)
    cleanup(0, mocked_username)
    assert user