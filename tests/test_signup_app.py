from playwright.sync_api import Page, expect
import pytest
from app import app
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User


"""
Ensures that the signup page is rendered correctly
"""


class TestUserRegistration:
    @pytest.fixture
    def client(self):
        app.config["TESTING"] = True
        client = app.test_client()
        yield client

    def test_signup_page(self, client):
        response = client.get("/register")
        assert b"Sign Up" in response.data

    def test_registration_email_exists(self, client):
        with app.app_context():
            user_repo = UserRepository(get_flask_database_connection(app))
            existing_user = User(
                id=1,
                name="Existing User",
                email="testuser@example.com",
                password="hashed_password",
            )
            user_repo.create(existing_user)

            data = {
                "first_name": "testuser",
                "last_name": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword",
            }
            response = client.post("/register", data=data, follow_redirects=True)
            assert b"An account with this email already exists." in response.data

    def test_registration_password_error(self, client):
        with app.app_context():
            user_repo = UserRepository(get_flask_database_connection(app))

            data = {
                "first_name": "testuser",
                "last_name": "testuser",
                "email": "newuser@example.com",
                "password": "weak",
            }
            response = client.post("/register", data=data, follow_redirects=True)
            assert response.status_code == 200
            assert (
                b"Password must have at least 8 characers, 1 number, and 1 special character."
                in response.data
            )
