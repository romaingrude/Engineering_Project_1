from lib.booking_repository import BookingRepository
from lib.booking import Booking

def test_constructs_booking_repository(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()

    assert bookings == [
        Booking(1, 1, 1, True, '2021-01-01', '2021-01-02'),
        Booking(2, 2, 2, False, '2021-01-01', '2021-01-02')
    ]


def test_create_a_single_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking = Booking(4, 1, 1, False, '2021-01-01', '2021-01-02')
    id = booking_respository.create_booking(booking)
    
    bookings = booking_respository.all()

    assert bookings == [
        Booking(1, 1, 1, True, '2021-01-01', '2021-01-02'),
        Booking(2, 2, 2, False, '2021-01-01', '2021-01-02'),
        Booking(3, 1, 1, False, '2021-01-01', '2021-01-02')
    ]

def test_deny_a_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking_respository.deny_booking(2) == None
    bookings = booking_respository.all()

    assert bookings == [
        Booking(1, 1, 1, True, '2021-01-01', '2021-01-02'),
        Booking(3, 1, 1, False, '2021-01-01', '2021-01-02')
    ]

def test_confirm_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking_respository.confirm_booking(2) == None
    bookings = booking_respository.all()

    assert bookings == [
        Booking(1, 1, 1, True, '2021-01-01', '2021-01-02'),
        Booking(2, 2, 2, True, '2021-01-01', '2021-01-02'),
        Booking(3, 1, 1, False, '2021-01-01', '2021-01-02')
    ]