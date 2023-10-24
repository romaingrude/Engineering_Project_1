from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""

def test_get_rooms(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([
        "Name: Room 1\nDescription: This is a room\nPrice: £100.0",
        "Name: Room 2\nDescription: This is another room\nPrice: £200.0",
    ])

def test_get_single_room(db_connection, page, test_web_address):
    db_connection.seed("seeds/MakersBNB_seed.sql")
    page.goto(f"http://{test_web_address}/rooms/1")
    div_tag = page.locator("div")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Room 1")
    expect(div_tag).to_have_text(["""Description: This is a room\nPrice: £100.0"""])