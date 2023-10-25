from lib.booking_repository import BookingRepository
from lib.booking import Booking
import datetime


def test_constructs_booking_repository(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()
    booking_1 = Booking(
        1, 1, 1, True, datetime.date(2023, 11, 1), datetime.date(2023, 11, 10)
    )
    booking_2 = Booking(
        2, 2, 2, False, datetime.date(2023, 11, 1), datetime.date(2023, 11, 15)
    )

    assert bookings == [booking_1, booking_2]


def test_create_a_single_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking = Booking(
        3, 1, 1, False, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)
    )
    id = booking_respository.create_booking(booking)

    bookings = booking_respository.all()
    booking_1 = Booking(
        1, 1, 1, True, datetime.date(2023, 11, 1), datetime.date(2023, 11, 10)
    )
    booking_2 = Booking(
        2, 2, 2, False, datetime.date(2023, 11, 1), datetime.date(2023, 11, 15)
    )
    booking_3 = Booking(
        3, 1, 1, False, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)
    )

    assert bookings == [booking_1, booking_2, booking_3]


def test_deny_a_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking_respository.deny_booking(2) == None
    bookings = booking_respository.all()
    booking_1 = Booking(
        1, 1, 1, True, datetime.date(2023, 11, 1), datetime.date(2023, 11, 10)
    )

    assert bookings == [
        booking_1,
    ]


def test_confirm_booking(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    booking_respository = BookingRepository(db_connection)

    booking_respository.confirm_booking(2) == None
    bookings = booking_respository.all()

    assert bookings == [
        Booking(1, 1, 1, True, datetime.date(2023, 11, 1), datetime.date(2023, 11, 10)),
        Booking(2, 2, 2, True, datetime.date(2023, 11, 1), datetime.date(2023, 11, 15)),
    ]
