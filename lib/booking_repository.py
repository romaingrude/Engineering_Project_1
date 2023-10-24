from lib.booking import Booking

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

    def confirm_booking(self, booking_id): #--> meaning accept request
        rows = self._connection.execute(
            'UPDATE bookings SET confirmation = True WHERE id = %s', [booking_id]
        )

    def deny_booking(self, booking_id): #--> meaning delete request
        rows = self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id])
        return None
    


    # rows = self._connection.execute("SELECT * from bookings")
    #     return [Booking(row["id"], row["user_id"], row["room_id"], row["confirmation"], row["booking_start"], row["booking_end"]) for row in rows]