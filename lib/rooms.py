class Rooms():
    def __init__(self, id, name, price, description, user_id):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Rooms({self.id}, {self.name}, {self.price}, {self.description}, {self.user_id})"
