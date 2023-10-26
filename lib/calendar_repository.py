from datetime import datetime


class CalendarRepository:
    def __init__(self, connection):
        self._connection = connection

    def add_booked_date(self, user_id, room_id, confirmation, start_date, end_date):
        self._connection.execute(
            "INSERT INTO bookings (user_id, room_id, confirmation, booking_start, booking_end) VALUES (%s, %s, %s, %s, %s)",
            [user_id, room_id, confirmation, start_date, end_date],
        )

    def get_booked_dates_for_room(self, room_id):
        rows = self._connection.execute(
            "SELECT booking_start, booking_end FROM bookings WHERE room_id = %s",
            [room_id],
        )
        booked_dates = []
        for row in rows:
            start_date = row["booking_start"]
            end_date = row["booking_end"]
            booked_dates.append([start_date, end_date])
        return booked_dates

    def is_date_booked(self, room_id, date):
        result = self._connection.execute(
            "SELECT COUNT(*) FROM bookings WHERE room_id = %s AND booking_start <= %s AND booking_end >= %s",
            [room_id, date, date],
        )
        row = result[0]
        return row["count"] > 0
