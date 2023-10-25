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

# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")

@app.route('/requests')
def get_albums():
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    requested = repository.all()
    requests = repository.all()
    return render_template("allBookings.html", requestedBookings=requested, bookingRequests=requests)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
