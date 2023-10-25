from lib.calendar_repository import CalendarRepository

"""
list dates booked for a room
"""


def test_calendar_constructs(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    calendar_repo = CalendarRepository(db_connection)
    booked_dates = calendar_repo.get_booked_dates_for_room(1)
    assert booked_dates == [["2023-11-01", "2023-11-10"]]


"""
Add a date to the booked dates for a room and then list the booked dates
"""


def test_calendar_add_then_list(db_connection):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    calendar_repo = CalendarRepository(db_connection)
    calendar_repo.add_booked_date(1, "2021-01-03", "2021-01-04")
    booked_dates = calendar_repo.get_booked_dates_for_room(1)
    assert booked_dates == [["2023-11-01", "2023-11-10"], ["2021-01-03", "2021-01-04"]]
