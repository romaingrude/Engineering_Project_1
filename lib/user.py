class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        return f"User({self.name}, {self.email}, {self.password})"
