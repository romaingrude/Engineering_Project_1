from lib.booking import Booking
import datetime

def test_constructs_booking():
    booking = Booking(1, 1, 1, True, '2021-01-01', '2021-01-02')
    assert booking.id == 1
    assert booking.user_id == 1
    assert booking.room_id == 1
    assert booking.confirmation == True
    assert booking.booking_start == '2021-01-01'
    assert booking.booking_end == '2021-01-02'

def test_booking_instances_match():
    booking_1 = Booking(1, 1, 1, True, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2))
    booking_2 = Booking(1, 1, 1, True, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2))
    assert booking_1 == booking_2

def test_booking_formats_nicely():
    booking = Booking(1, 1, 1, True, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2))
    assert str(booking) == "Booking(1, 1, 1, True, 2021-01-01, 2021-01-02)"