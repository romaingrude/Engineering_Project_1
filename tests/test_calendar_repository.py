from lib.calendar_repository import CalendarRepository
from datetime import date

"""
list dates booked for a room
"""


def test_calendar_constructs(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    calendar_repo = CalendarRepository(db_connection)
    booked_dates = calendar_repo.get_booked_dates_for_room(1)
    assert booked_dates == [[date(2023, 11, 1), date(2023, 11, 10)]]


"""
Add a date to the booked dates for a room and then list the booked dates
"""


def test_calendar_add_then_list(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    calendar_repo = CalendarRepository(db_connection)
    calendar_repo.add_booked_date(1, 1, False, "2021-01-03", "2021-01-04")
    booked_dates = calendar_repo.get_booked_dates_for_room(1)
    assert booked_dates == [
        [date(2023, 11, 1), date(2023, 11, 10)],
        [date(2021, 1, 3), date(2021, 1, 4)],
    ]
