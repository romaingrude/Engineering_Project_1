from lib.rooms_repository import RoomsRepository
from lib.rooms import Rooms

def test_all_rooms_are_shown(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repo = RoomsRepository(db_connection)

    rooms = repo.all()

    assert rooms == [
        Rooms(1, 'Room 1', 100, 'This is a room', 1),
        Rooms(2, 'Room 2', 200, 'This is another room', 2)
    ]

def test_find_a_single_room(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repo = RoomsRepository(db_connection)

    room = repo.find(1)

    assert room == Rooms(1, 'Room 1', 100, 'This is a room', 1)

def test_list_a_room(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repo = RoomsRepository(db_connection)

    repo.create(Rooms(None, 'Room 3', 300, 'This is the third room', 2))
    result = repo.all()

    assert result == [
        Rooms(1, 'Room 1', 100, 'This is a room', 1),
        Rooms(2, 'Room 2', 200, 'This is another room', 2),
        Rooms(3, 'Room 3', 300, 'This is the third room', 2)
    ]

def test_delete_a_room(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repo = RoomsRepository(db_connection)

    repo.delete(1)
    result = repo.all()
    assert result == [
        Rooms(2, 'Room 2', 200, 'This is another room', 2),
        ]
