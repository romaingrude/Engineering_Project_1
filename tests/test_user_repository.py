from lib.user_repository import UserRepository
from lib.user import User
import hashlib

"""
When I call UserRepository.all() it returns a list of users
"""


def test_user_repo_all(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    repo = UserRepository(db_connection)

    assert repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
    ]


"""
When I call UserRepository.create() it creates a new user
"""


def test_user_repo_create(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    user_repo = UserRepository(db_connection)

    new_user = User(None, "Romain", "romaingrude@yahoo.fr", "testpassword")
    user_repo.create(new_user)

    # Get the created user from the repository
    users = user_repo.all()
    created_user = users[-1]

    # Check if the password is encrypted
    assert created_user.password != "testpassword"
    assert (
        hashlib.sha256("testpassword".encode("utf-8")).hexdigest()
        == created_user.password
    )
    assert users == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(3, "Romain", "romaingrude@yahoo.fr", created_user.password),
    ]


"""
When I call UserRepository.find_by_email() it returns the user with the given email
"""


def test_user_repo_find_by_email(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    user_repo = UserRepository(db_connection)

    assert user_repo.find_by_email("test2@gmail.com") == User(
        2, "Jane", "test2@gmail.com", "1234"
    )

    assert user_repo.find_by_email("non-existing@gmail.com") == None


"""
When I call UserRepository.check_password() it returns True if the password is correct and False otherwise
"""


def test_user_repo_check_password(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    user_repo = UserRepository(db_connection)
    new_user = User(None, "Romain", "romaingrude@yahoo.fr", "testpassword")
    user_repo.create(new_user)
    assert user_repo.check_password("romaingrude@yahoo.fr", "testpassword") == True
    assert user_repo.check_password("romaingrude@yahoo.fr", "wrongpassword") == False


"""
When I call UserRepository.update() it updates the user with the given email
"""


def test_user_repo_update(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    user_repo = UserRepository(db_connection)

    user1 = User(None, "Romain", "romaingrude@yahoo.fr", "testpassword")
    user_repo.create(user1)

    hashed_password = hashlib.sha256("testpassword".encode("utf-8")).hexdigest()
    # First create a user
    assert user_repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(3, "Romain", "romaingrude@yahoo.fr", hashed_password),
    ]
    # Then update it, name and email
    user_repo.update("romaingrude@yahoo.fr", "Romain Grude", "new@gmail.com")

    # Check if the user has been updated
    assert user_repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(3, "Romain Grude", "new@gmail.com", hashed_password),
    ]

    # Then update it, only name
    user_repo.update("new@gmail.com", "TESTNAME")

    assert user_repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(3, "TESTNAME", "new@gmail.com", hashed_password),
    ]

    # then update it, only password
    user_repo.update("new@gmail.com", new_password="newpassword")

    hashed_new = hashlib.sha256("newpassword".encode("utf-8")).hexdigest()
    assert user_repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(3, "TESTNAME", "new@gmail.com", hashed_new),
    ]


"""
When I call UserRepository.delete() it deletes the user with the given email if password if correct
"""


def test_user_repo_delete(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")

    user_repo = UserRepository(db_connection)

    user1 = User(None, "Romain", "testemail@gmail.com", "testpassword")
    user_repo.create(user1)
    user2 = User(None, "Tristan", "emailtest@yahoo.com", "123321")
    user_repo.create(user2)

    hashed_password_user2 = hashlib.sha256("123321".encode("utf-8")).hexdigest()

    user_repo.delete("testemail@gmail.com", "testpassword")

    assert user_repo.all() == [
        User(1, "John", "test@gmail.com", "1234"),
        User(2, "Jane", "test2@gmail.com", "1234"),
        User(4, "Tristan", "emailtest@yahoo.com", hashed_password_user2),
    ]
