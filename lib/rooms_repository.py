from lib.rooms import Rooms


class RoomsRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM rooms")
        rooms = []
        for row in rows:
            item = Rooms(
                row["id"], row["name"], row["price"], row["description"], row["user_id"]
            )
            rooms.append(item)
        return rooms

    def find(self, room_id):
        rows = self._connection.execute("SELECT * FROM rooms WHERE id = %s", [room_id])
        row = rows[0]
        return Rooms(
            row["id"], row["name"], row["price"], row["description"], row["user_id"]
        )

    def create(self, room):
        self._connection.execute(
            "INSERT INTO rooms (name, price, description, user_id) VALUES(%s, %s, %s, %s)",
            [room.name, room.price, room.description, room.user_id],
        )
        return None

    def delete(self, id):
        self._connection.execute("DELETE FROM rooms WHERE id = %s", [id])
        return None

    def get_rooms_paginated(self, offset, limit):
        rows = self._connection.execute(
            "SELECT * FROM rooms LIMIT %s OFFSET %s", [limit, offset]
        )
        rooms = []
        for row in rows:
            item = Rooms(
                row["id"], row["name"], row["price"], row["description"], row["user_id"]
            )
            rooms.append(item)
        return rooms

    def get_total_rooms_count(self):
        # Assume the connection supports iterating through rows
        rows = self._connection.execute("SELECT COUNT(*) AS count FROM rooms")
        for row in rows:
            return row["count"]
