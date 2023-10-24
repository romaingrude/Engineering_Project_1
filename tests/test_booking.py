from lib.booking import Booking

def test_constructs_booking():
    booking = Booking(1, 1, 1, True, '2021-01-01', '2021-01-02')
    assert booking.id == 1
    assert booking.user_id == 1
    assert booking.room_id == 1
    assert booking.confirmation == True
    assert booking.booking_start == '2021-01-01'
    assert booking.booking_end == '2021-01-02'

def test_booking_instances_match():
    booking_1 = Booking(1, 1, 1, True, '2021-01-01', '2021-01-02')
    booking_2 = Booking(1, 1, 1, True, '2021-01-01', '2021-01-02')
    assert booking_1 == booking_2

def test_booking_formats_nicely():
    booking = Booking(1, 1, 1, True, '2021-01-01', '2021-01-02')
    assert str(booking) == "Booking(1, 1, 1, True, 2021-01-01, 2021-01-02)"