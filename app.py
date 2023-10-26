import os
from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    flash,
)
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


@app.route("/rooms/<id>/booking_request/", methods=["GET"])
def booking_request(id):
    connection = get_flask_database_connection(app)
    room_repo = RoomsRepository(connection)
    room = room_repo.find(id)

    # Calculate the minimum date (today)
    min_date = date.today().isoformat()

    # Fetch the booked dates for this room using CalendarRepository
    calendar_repo = CalendarRepository(connection)
    booked_dates_list = calendar_repo.get_booked_dates_for_room(room.id)

    # Format the dates as YYYY-MM-DD
    formatted_booked_dates = [
        [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
        for start_date, end_date in booked_dates_list
    ]

    # Create the booked_dates_dic dictionary
    booked_dates_dic = {}
    for i, date_range in enumerate(formatted_booked_dates, start=1):
        start_date, end_date = date_range
        booked_dates_dic[i] = {"start": start_date, "end": end_date}

    form = InfoForm()  # Instantiate the form
    return render_template(
        "rooms/room_book.html",
        room=room,
        min_date=min_date,
        booked_dates=booked_dates_dic,
        form=form,
    )


@app.route("/booking", methods=["POST"])
def booking():
    if request.method == "POST":
        start_date = request.form["startdate"]
        end_date = request.form["enddate"]

        # Convert the date strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Retrieve user ID from the session
        user_id = session.get("user_id")
        room_id = session.get("room_id")

        if user_id is not None:
            # Add the booking to the database
            connection = get_flask_database_connection(app)
            calendar_repo = CalendarRepository(connection)
            calendar_repo.add_booked_date(user_id, room_id, False, start_date, end_date)
            session["booking_complete"] = True
            flash("Booking was successful!", "success")
            return redirect(url_for("get_rooms"))

        else:
            # Handle the case where the user is not logged in
            # You can display an error message or redirect to the login page
            return redirect(url_for("login"))


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


from datetime import date, timedelta


@app.route("/rooms/<id>", methods=["GET"])
def get_single_room(id):
    connection = get_flask_database_connection(app)
    room_repo = RoomsRepository(connection)
    room = room_repo.find(id)

    session["room_id"] = room.id

    return render_template(
        "rooms/room_show.html",
        room=room,
    )


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
