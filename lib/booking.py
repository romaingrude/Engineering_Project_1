class Booking:
    def __init__(self, id, user_id, room_id, confirmation, booking_start, booking_end):
        self.id = id
        self.user_id = user_id
        self.room_id = room_id
        self.confirmation = confirmation
        self.booking_start = booking_start
        self.booking_end = booking_end

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.id}, {self.user_id}, {self.room_id}, {self.confirmation}, {self.booking_start}, {self.booking_end})"