from lib.booking import Booking
from lib.request import Request

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

    def getRequestedByUserId(self, userId):
        rows = self._connection.execute('SELECT b.id, b.user_id, b.room_id, b.confirmation, b.booking_start, r.name '
                                        'FROM bookings AS b ' 
                                        'INNER JOIN rooms AS r '
                                        'ON b.room_id = r.id '
                                        'WHERE b.user_id = %i' % userId)
        requests = []
        for row in rows:
            item = Request(row["id"], row["user_id"], row["name"], row["confirmation"], row["booking_start"])
            requests.append(item)
        return requests
    
    def getRequestsForUserId(self, userId):
        rows = self._connection.execute('SELECT b.id, r.user_id, b.room_id, b.confirmation, b.booking_start, r.name '
                                        'FROM bookings AS b ' 
                                        'INNER JOIN rooms AS r '
                                        'ON b.room_id = r.id '
                                        'WHERE r.user_id = %i' % userId) 
        requests = []
        for row in rows:
            item = Request(row["id"], row["user_id"], row["name"], row["confirmation"], row["booking_start"])
            requests.append(item)
        return requests

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