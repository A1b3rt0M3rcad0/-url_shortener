from datetime import datetime, timezone
import pytest
from sqlalchemy import text
from src.infra.db.repositories.urls_repository import UrlsRepository
from src.infra.db.settings.connection import DBConnectionHandler

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine()

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

    return get_user_id(username)

def get_user_id(username):
    sql = 'SELECT id FROM users WHERE username = :username'
    with connection.connect() as conn:
        response = conn.execute(text(sql), {"username": username})
        return response.scalar()  # Retorna apenas o valor da primeira coluna

def get_url(user_id):
    sql = 'SELECT link, shortened_link FROM urls WHERE user_id = :user_id'
    with connection.connect() as conn:
        return conn.execute(text(sql), {"user_id": user_id}).fetchone()

def cleanup(user_id, username):
    with connection.connect() as conn:
        conn.execute(text('DELETE FROM urls WHERE user_id = :user_id'), {"user_id": user_id})
        conn.execute(text('DELETE FROM users WHERE username = :username'), {"username": username})
        conn.commit()

@pytest.mark.skip('Sensitive Test')
def test_create_url():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_url = 'http://www.example.com'
    mocked_shortened_url = 'http://shorte.me'

    user_id = insert_user(mocked_username, mocked_password, 1, datetime.now(timezone.utc))

    urls_repository = UrlsRepository(DBConnectionHandler)
    urls_repository.create(user_id=user_id, link=mocked_url, shortened_link=mocked_shortened_url)

    registry = get_url(user_id)

    cleanup(user_id, mocked_username)

    assert registry.link == mocked_url
    assert registry.shortened_link == mocked_shortened_url