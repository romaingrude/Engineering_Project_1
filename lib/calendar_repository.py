from datetime import datetime


class CalendarRepository:
    def __init__(self, connection):
        self._connection = connection

    def add_booked_date(self,user_id, room_id, start_date, end_date):
        self._connection.execute(
            "INSERT INTO bookings (room_id, booking_start, booking_end) VALUES (%s, %s, %s)",
            [room_id, start_date, end_date],
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
