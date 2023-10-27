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
            "Name: Room 1\nDescription: This is a room\nPrice: £100.0",
            "Name: Room 2\nDescription: This is another room\nPrice: £200.0",
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
    page.fill("input[name=description]", "This is the third room.")
    page.fill("input[name=price]", "300")
    page.fill("input[name=start_date]", "2021-12-12")
    page.fill("input[name=end_date]", "2021-12-17")

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
