import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.rooms_repository import RoomsRepository
import secrets
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from datetime import datetime
from lib.calendar_repository import CalendarRepository

# Create a new Flask app
app = Flask(__name__)

# Generate a secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask app
app.secret_key = secret_key


class InfoForm(FlaskForm):
    startdate = DateField(
        "Start Date", format="%Y-%m-%d", validators=(validators.DataRequired(),)
    )
    enddate = DateField(
        "End Date", format="%Y-%m-%d", validators=(validators.DataRequired(),)
    )
    submit = SubmitField("Submit")


# Custom filter to format the date
def format_date(date):
    if isinstance(date, str):
        date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    return date.strftime("%Y-%m-%d")


# Add the custom filter to the Jinja2 environment
app.jinja_env.filters["format_date"] = format_date


@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    startdate = session["startdate"]
    enddate = session["enddate"]
    return render_template("confirmation.html")


# Rest of your code...


# @app.route("/index", methods=["GET"])
# def get_index():
#     return render_template("index.html")


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


@app.route("/rooms", methods=["GET"])
def get_rooms():
    connection = get_flask_database_connection(app)
    repo = RoomsRepository(connection)
    rooms = repo.all()
    return render_template("rooms/room_index.html", rooms=rooms)


@app.route("/rooms/<id>", methods=["GET"])
def get_single_room(id):
    connection = get_flask_database_connection(app)
    room_repo = RoomsRepository(connection)
    room = room_repo.find(id)

    # Calculate the minimum date (today)
    min_date = datetime.now().date()

    # Fetch the booked dates for this room using CalendarRepository
    calendar_repo = CalendarRepository(connection)
    booked_dates = [
        [date.strftime("%Y-%m-%d") for date in range]
        for range in calendar_repo.get_booked_dates_for_room(room.id)
    ]
    print(min_date)  # Add this line to check min_date value
    return render_template(
        "rooms/room_show.html",
        room=room,
        min_date=min_date,
        booked_dates=[str(date) for date in booked_dates],
    )


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
