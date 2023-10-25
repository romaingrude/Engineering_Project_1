import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.rooms import Rooms
from lib.rooms_repository import RoomsRepository
from lib.booking import Booking
from lib.booking_repository import BookingRepository
import secrets

# Create a new Flask app
app = Flask(__name__)

# Generate a secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask app
app.secret_key = secret_key


@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")

# LOGIN
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    errors = []

    if not email:
        errors.append("Email is required.")
    if not password:
        errors.append("Password is required.")

    # Create an instance of UserRepository
    user_repo = UserRepository(get_flask_database_connection(app))

    if not errors:
        if user_repo.check_password(email, password):
            user = user_repo.find_by_email(email)
            # Set the user ID in session
            session["user_id"] = user.id

            return redirect(url_for("temp_account"))
        else:
            errors.append("Invalid login details.")

    return render_template("login.html", error_message=" ".join(errors))

@app.route("/temp")
def temp_account():
    if "user_id" not in session:
        # No user id in the session so the user is not logged in.
        return redirect("/login")
    else:
        # The user is logged in, display their account page.
        return render_template("temp.html")

# ROOMS
@app.route("/rooms", methods=["GET"])
def get_rooms():
    connection = get_flask_database_connection(app)
    repo = RoomsRepository(connection)
    rooms = repo.all()
    return render_template("rooms/room_index.html", rooms=rooms)

@app.route('/rooms/<id>', methods = ['GET'])
def get_single_room(id):
    connection = get_flask_database_connection(app)
    room_repo = RoomsRepository(connection)
    room = room_repo.find(id)

    return render_template("rooms/room_show.html", room=room)

# BOOKINGS
@app.route("/bookings/<booking_id>", methods=["GET"])
def get_room_name_and_description_and_other_requests(booking_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking = booking_repository.find_with_room(booking_id)
    user = booking_repository.find_with_user(booking_id)
    bookings = booking_repository.find_all_bookings_for_this_room(booking_id)
    return render_template("bookings/show.html", booking=booking, user=user, bookings=bookings)



# [(Booking(1, 1, 1, True, 2021-01-01, 2021-01-02), Rooms(1, Room 1, 100.0, This is a room, 1))]

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))

