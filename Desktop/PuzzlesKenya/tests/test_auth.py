import pytest 
from flask import g, session
from puzzleske.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code==200
    response = client.post(
        '/auth/register',
        data = {
            'username': 'a',
            'password': 'a',
            'email': 'a',
        }
    )
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username='a'"
        ).fetchone()
        assert user is not None


@pytest.mark.parametrize(('username', 'password', 'email', 'message'),(
    ('', '', '', b'Username is required'),
    ('a', '', '', b'Password is required'),
    ('test', 'test', '', b'Username is already taken.'),
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/auth/register',
        data={
            'username': username,
            'password': password,
            'email': email,
        }
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code==200
    response = auth.login()
    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Check your username.'),
    ('test', 'a', b'Check your password'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session 