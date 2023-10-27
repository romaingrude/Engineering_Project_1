class Request:
    def __init__(self, id, user_id, name, confirmation, booking_start, ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.confirmation = confirmation
        self.booking_start = booking_start

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.id}, {self.user_id}, {self.name}, {self.confirmation}, {self.booking_start})"