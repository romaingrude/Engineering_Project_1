from playwright.sync_api import Page, expect
import pytest
from app import app
from lib.user_repository import UserRepository
from lib.rooms_repository import RoomsRepository
from lib.user import User
from lib.rooms import Rooms

# Tests for your routes go here

"""
Ensures that the signup page is rendered correctly
"""
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup_page(client):
    response = client.get('/')
    assert b'Sign Up' in response.data
    assert b'Name:' in response.data
    assert b'Email:' in response.data
    assert b'Password:' in response.data
    assert b'Sign Up' in response.data

def test_registration(client):
    data = {
        'name': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert b'Registration Successful' in response.data

