from lib.booking_repository import BookingRepository
from lib.booking import Booking

def test_constructs_booking_repository(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    bookings = booking_respository.all()

    assert bookings == [
        Booking(1, 1, 1, True, '2021-01-01', '2021-01-02'),
        Booking(2, 2, True, '2021-01-01', '2021-01-02')
    ]