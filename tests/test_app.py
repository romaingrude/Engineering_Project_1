from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User

"""
We can render the index page
"""

def test_get_rooms(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text([
        "Name: Room 1\nDescription: This is a room\nPrice: £100.0",
        "Name: Room 2\nDescription: This is another room\nPrice: £200.0"
    ])

def test_get_single_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms/1")
    p_tag = page.locator("p")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Room 1")
    expect(p_tag).to_have_text(["""Description: This is a room\nPrice: £100.0"""])

def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look at the <p> tag
    strong_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(strong_tag).to_have_text("This is the homepage.")

# Bookings
def test_get_room_name_and_description(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=Request for 'Room 1'")
    page.click("text=This is a room")
    title_element = page.locator(".title")
    description_element = page.locator(".description")
    expect(title_element).to_have_text("Request for 'Room 1'")
    expect(description_element).to_have_text("This is a room")

def test_get_all_confirmed_bookings_for_the_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=Confirmed")
    confirmation_element = page.locator(".confirmation")
    expect(confirmation_element).to_have_text("Confirmed")

def test_get_all_not_confirmed_bookings_for_the_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/2")
    page.click("text=Not confirmed")
    confirmation_element = page.locator(".confirmation")
    expect(confirmation_element).to_have_text("Not confirmed")

def test_get_user_details(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=From: test@gmail.com")
    email_element = page.locator(".user_email")
    expect(email_element).to_have_text("From: test@gmail.com")
    
def test_get_booking_date(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=Date: 2021-01-01")
    date_element = page.locator(".booking_date")
    expect(date_element).to_have_text("Date: 2021-01-01")
    
def test_get_number_of_bookings(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=No. of Spaces booked: 1")
    spaces_booked_element = page.locator(".spaces_booked")
    expect(spaces_booked_element).to_have_text("No. of Spaces booked: 1")

def test_post_confirm_booking(db_connection, web_client):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    response = web_client.post("/bookings", data={'id': 2, 'user_id': 2, 'confirmation': 'False', 'booking_start': '2021-01-01', 'booking_end': '2021-01-02'})
    assert response.status_code == 200

# Booking(row["id"], row["user_id"], None, row["confirmation"], row["booking_start"], row["booking_end"])
# (2, 2, False, '2021-01-01', '2021-01-02')

class TestLogin:

    """
    We can render the login page
    """

    def test_get_login_page(self, page, test_web_address):
        page.goto(f"http://{test_web_address}/login")

        h1_tag = page.locator("h1")

        expect(h1_tag).to_have_text("Account Login")

    """
    When we enter the incorrect credentials, we are redirected to the error page
    """

    def test_login_post_incorrect_credentials(
        self, page, test_web_address, db_connection
    ):
        page.goto(f"http://{test_web_address}/login")
        page.fill("input[name=email]", "wrong@gmail.com")
        page.fill("input[name=password]", "random")
        page.click("text=Log in")

        h1_tag = page.locator("h1")
        expect(h1_tag).to_have_text("Account Login")

    """
    When we enter the correct credentials, we are redirected to the temp page
    """

    def test_login_post_correct_credentials(
        self, page, test_web_address, db_connection
    ):
        # First we create a new user in order to test the hashed password
        db_connection.seed("seeds/MakersBNB_seed.sql")
        user_repo = UserRepository(db_connection)
        user = User(None, "Romain", "emailtest@gmail.com", "12345")
        user_repo.create(user)

        page.goto(f"http://{test_web_address}/login")
        page.fill("input[name=email]", "emailtest@gmail.com")
        page.fill("input[name=password]", "12345")
        page.click("text=Log in")

        h1_tag = page.locator("h1")
        expect(h1_tag).to_have_text("Login Successful")
