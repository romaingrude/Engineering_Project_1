from lib.user import User

"""
Initially constructs the User object
"""


def test_user_constructs():
    user = User(1, "Romain", "romaingrude@yahoo.fr", "testpassword")
    assert user.id == 1
    assert user.name == "Romain"
    assert user.email == "romaingrude@yahoo.fr"
    assert user.password == "testpassword"


"""
Check two users are equal
"""


def test_user_equal():
    user1 = User(1, "Romain", "romaingrude@yahoo.fr", "testpassword")
    user2 = User(1, "Romain", "romaingrude@yahoo.fr", "testpassword")
    assert user1 == user2


"""
Test user format
"""


def test_user_format():
    user = User(1, "Romain", "romaingrude@yahoo.fr", "testpassword")
    assert str(user) == "User(1, Romain, romaingrude@yahoo.fr, testpassword)"
