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

def insert_url(user_id, link, shortened_link):
    sql = '''
    INSERT INTO urls (user_id, link, shortened_link)
    VALUES (:user_id, :link, :shortened_link)
    '''
    with connection.connect() as conn:
        conn.execute(text(sql),{
            'user_id': user_id,
            'link': link,
            'shortened_link': shortened_link
        })
        conn.commit()

def get_user_id(username):
    sql = 'SELECT id FROM users WHERE username = :username'
    with connection.connect() as conn:
        response = conn.execute(text(sql), {"username": username})
        return response.scalar()  # Retorna apenas o valor da primeira coluna

def get_url(user_id):
    sql = 'SELECT id, link, shortened_link FROM urls WHERE user_id = :user_id'
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

@pytest.mark.skip('Sensitive Test')
def test_select_url():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_url = 'http://www.example.com'
    mocked_shortened_url = 'http://shorte.me'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    insert_user(mocked_username, 
                mocked_password, 
                mocked_is_active, 
                mocked_created_at)
    user_id = get_user_id(mocked_username)
    insert_url(user_id, mocked_url, mocked_shortened_url)

    urls_repository = UrlsRepository(DBConnectionHandler)
    urls = urls_repository.select(user_id)

    cleanup(user_id, mocked_username)

    assert urls[0].user_id == user_id
    assert urls[0].link == mocked_url
    assert urls[0].shortened_link == mocked_shortened_url

@pytest.mark.skip('Sensitive Test')
def test_delete_url():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_url = 'http://www.example.com'
    mocked_shortened_url = 'http://shorte.me'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    insert_user(mocked_username, 
                mocked_password, 
                mocked_is_active, 
                mocked_created_at)
    user_id = get_user_id(mocked_username)
    insert_url(user_id, mocked_url, mocked_shortened_url)

    url = get_url(user_id)

    urls_repository = UrlsRepository(DBConnectionHandler)
    urls_repository.delete(url[0])

    test_url = get_url(user_id)

    cleanup(user_id, mocked_username)

    assert not test_url

@pytest.mark.skip('Sensitive Test')
def test_update_url():
    mocked_username = 'username'
    mocked_password = 'password'
    mocked_url = 'http://www.example.com'
    mocked_shortened_url = 'http://shorte.me'
    mocked_is_active = 1
    mocked_created_at = datetime.now(timezone.utc)
    insert_user(mocked_username, 
                mocked_password, 
                mocked_is_active, 
                mocked_created_at)
    user_id = get_user_id(mocked_username)
    insert_url(user_id, mocked_url, mocked_shortened_url)

    url = get_url(user_id)

    urls_repository = UrlsRepository(DBConnectionHandler)
    update_params = {
        'link': 'http://www.google.com'
    }
    urls_repository.update(url[0], update_params)

    edited_url = get_url(user_id)
    new_link = edited_url[1]

    cleanup(user_id, mocked_username)

    assert new_link == update_params['link']