from lib.rooms import Rooms

def test_rooms_constructs():
    rooms = Rooms(1, "Room 1", 2500, "This a room", 1)
    assert rooms.id == 1
    assert rooms.name == 'Room 1'
    assert rooms.price == 2500
    assert rooms.description == "This a room"
    assert rooms.user_id == 1