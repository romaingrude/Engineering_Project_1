from lib.user import User
import hashlib


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        users = [
            User(row["id"], row["name"], row["email"], row["password"]) for row in rows
        ]
        return users

    def create(self, name, email, password):
        binary_password = password.encode("utf-8")
        hashed_password = hashlib.sha256(binary_password).hexdigest()

        self._connection.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            [name, email, hashed_password],
        )

    def check_password(self, email, password_attempt):
        # Hash the password attempt
        binary_password_attempt = password_attempt.encode("utf-8")
        hashed_password_attempt = hashlib.sha256(binary_password_attempt).hexdigest()

        # Check whether there is a user in the database with the given email
        # and a matching password hash, using a SELECT statement.
        rows = self._connection.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            [email, hashed_password_attempt],
        )
        print(f"DEBUG {rows}")
        # If that SELECT finds any rows, the password is correct.
        return len(rows) > 0

    def find_by_email(self, email):
        rows = self._connection.execute("SELECT * FROM users WHERE email = %s", [email])
        if len(rows) == 0:
            return None
        else:
            row = rows[0]
            return User(row["id"], row["name"], row["email"], row["password"])

    def update(self, user_email, new_name=None, new_email=None, new_password=None):
        if new_name is not None:
            self._connection.execute(
                "UPDATE users SET name = %s WHERE email = %s", [new_name, user_email]
            )
        if new_email is not None:
            self._connection.execute(
                "UPDATE users SET email = %s WHERE email = %s", [new_email, user_email]
            )
        if new_password is not None:
            binary_password = new_password.encode("utf-8")
            hashed_password = hashlib.sha256(binary_password).hexdigest()
            self._connection.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                [hashed_password, user_email],
            )

    def delete(self, email, password):
        if self.check_password(email, password):
            self._connection.execute("DELETE FROM users WHERE email = %s", [email])
        return None
