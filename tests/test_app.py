from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User

# Tests for your routes go here

"""
We can render the index page
"""


def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look at the <p> tag
    strong_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(strong_tag).to_have_text("This is the homepage.")


"""
We can render the login page
"""


def test_get_login_page(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    h1_tag = page.locator("h1")

    expect(h1_tag).to_have_text("Account Login")


"""
When we enter the incorrect credentials, we are redirected to the error page
"""


def test_login_post_incorrect_credentials(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "wrong@gmail.com")
    page.fill("input[name=password]", "random")
    page.click("text=Log in")

    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Account Login")


"""
When we enter the correct credentials, we are redirected to the temp page
"""


def test_login_post_correct_credentials(page, test_web_address, db_connection):
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
