from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User
import time

"""
We can render the index page
"""


def test_get_rooms(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text(
        [
            "This is a room",
            "Price/night: £100.0",
            "This is another room",
            "Price/night: £200.0",
        ]
    )


def test_get_single_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms/1")
    p_tag = page.locator(
        ".room-details"
    )  # Update the locator to target the specific p tag with the custom class
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Room 1")
    expect(p_tag).to_have_text(["""Description: This is a room\nPrice: £100.0"""])


def test_create_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms")

    page.set_default_timeout(1000)
    # Click the button with a valid CSS selector
    page.click('button:has-text("List a Space")')

    h1new_tag = page.locator("h1")
    expect(h1new_tag).to_have_text("List a Space")

    page.fill("input[name=name]", "Room 3")
    page.fill("textarea[name=description]", "This is the third room.")
    page.fill("input[name=price]", "300")

    # Click the button with a valid CSS selector
    page.click("text=List my Space")

    h1rooms_tag = page.locator("h1")
    expect(h1rooms_tag).to_have_text("Book a Space")


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


def test_get_all_not_confirmed_bookings_for_the_room(
    db_connection, page, test_web_address
):
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
    page.click("text=Date: 2023-11-01")
    date_element = page.locator(".booking_date")
    expect(date_element).to_have_text("Date: 2023-11-01")


def test_get_number_of_bookings(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/bookings/1")
    page.click("text=No. of Spaces booked: 1")
    spaces_booked_element = page.locator(".spaces_booked")
    expect(spaces_booked_element).to_have_text("No. of Spaces booked: 1")


class TestLogin:

    """
    We can render the login page
    """

    def test_get_login_page(self, page, test_web_address):
        page.goto(f"http://{test_web_address}/login")

        h1_tag = page.locator("h1")

        expect(h1_tag).to_have_text("Account Login")

    """
    When we enter the incorrect credentials, we an error message
    """

    def test_login_post_incorrect_credentials(
        self, page, test_web_address, db_connection
    ):
        page.goto(f"http://{test_web_address}/login")
        page.fill("input[name=email]", "wrong@gmail.com")
        page.fill("input[name=password]", "random")
        page.click(".test-log-in")

        p_tag = page.locator("p")
        expect(p_tag).to_have_text("Invalid login details.")

    """
    When we try to login without entering any credentials, we get an error message
    """

    def test_login_post_empty_credentials(self, page, test_web_address, db_connection):
        page.goto(f"http://{test_web_address}/login")
        page.click(".test-log-in")

        p_tag = page.locator("p")
        expect(p_tag).to_have_text("Email is required. Password is required.")

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
        h1_tag = page.locator("h1")
        page.click(".test-log-in")
        h1_tag = page.locator("h1")
        expect(h1_tag).to_have_text("Book a Space")
