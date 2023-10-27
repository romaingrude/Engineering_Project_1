from lib.booking import Booking
from lib.rooms import Rooms
from lib.user import User

class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        bookings = []
        for row in rows:
            item = Booking(row["id"], row["user_id"], row["room_id"], row["confirmation"], row["booking_start"], row["booking_end"])
            bookings.append(item)
        return bookings

    def create_booking(self, booking):
        id = self._connection.execute(
            'INSERT INTO bookings (user_id, room_id, confirmation, booking_start, booking_end) VALUES (%s, %s, %s, %s, %s) RETURNING id', [booking.user_id, booking.room_id, booking.confirmation, booking.booking_start, booking.booking_end])
        return id

    def find_with_room(self, booking_id):
        rows = self._connection.execute(
            "SELECT bookings.id, bookings.confirmation, bookings.booking_start, bookings.booking_end, rooms.id AS room_id, rooms.name, rooms.price, rooms.description, rooms.user_id FROM bookings JOIN rooms ON rooms.id = bookings.room_id WHERE bookings.id = %s", [booking_id])
        for row in rows:
            room = Rooms(row["id"], row["name"], row["price"], row["description"], row["user_id"])
            return (Booking(row["id"], row["user_id"], row["room_id"], row["confirmation"], row["booking_start"], row["booking_end"]), room)
    
    def find_with_user(self, booking_id):
        rows = self._connection.execute(
            "SELECT bookings.id, bookings.confirmation, bookings.booking_start, bookings.booking_end, users.id AS user_id, users.name, users.email, users.password FROM bookings JOIN users ON users.id = bookings.user_id WHERE bookings.id = %s", [booking_id])
        for row in rows:
            user = User(row["id"], row["name"], row["email"], row["password"])
            return user
        
    def find_all_bookings_for_this_room(self, booking_id):
        rows = self._connection.execute(
            "SELECT bookings.id, bookings.confirmation, bookings.booking_start, bookings.booking_end, rooms.id AS room_id, rooms.name, rooms.price, rooms.description, rooms.user_id FROM bookings JOIN rooms ON rooms.id = bookings.room_id WHERE bookings.id = %s", [booking_id])
        bookings = []
        for row in rows:
            item = Booking(row["id"], row["user_id"], row["room_id"], row["confirmation"], row["booking_start"], row["booking_end"])
            room = Rooms(row["id"], row["name"], row["price"], row["description"], row["user_id"])
            if item.room_id == room.id:
                bookings.append((item, room))
        return bookings
    
    def count_bookings_for_this_user(self, booking_id):
        rows = self._connection.execute(
            "SELECT bookings.id, bookings.confirmation, bookings.booking_start, bookings.booking_end, users.id AS user_id, users.name, users.email, users.password FROM bookings JOIN users ON users.id = bookings.user_id WHERE bookings.id = %s", [booking_id])
        bookings = []
        for row in rows:
            item = Booking(row["id"], row["user_id"], None, row["confirmation"], row["booking_start"], row["booking_end"])
            user = User(row["id"], row["name"], row["email"], row["password"])
            if item.user_id == user.id:
                bookings.append(item)
        return len(bookings)

    def confirm_booking(self, booking_id): #--> meaning accept request
        rows = self._connection.execute(
            'UPDATE bookings SET confirmation = True WHERE id = %s', [booking_id]
        )
        return None

    def deny_booking(self, booking_id): #--> meaning delete request
        rows = self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id])
        return None
    


    # rows = self._connection.execute("SELECT * from bookings")
    #     return [Booking(row["id"], row["user_id"], row["room_id"], row["confirmation"], row["booking_start"], row["booking_end"]) for row in rows]