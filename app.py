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
from lib.booking_repository import BookingRepository
import secrets
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from datetime import datetime, date, timedelta
from lib.calendar_repository import CalendarRepository
from lib.user import User
from lib.rooms import Rooms


app = Flask(__name__)


#   ; open http://localhost:5000/index


@app.route("/register")
def signup():
    return render_template("signup.html")


@app.route("/register", methods=["POST"])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    user_repo = UserRepository(get_flask_database_connection(app))

    full_name = f"{first_name} {last_name}"

    existing_user = user_repo.find_by_email(email)

    if existing_user:
        return render_template(
            "signup.html", email_error="An account with this email already exists."
        )

    if (
        len(password) < 8
        or not any(char.isdigit() for char in password)
        or not any(char in "!@#$%^&*" for char in password)
    ):
        return render_template(
            "signup.html", password_error="Password does not meet the requirements."
        )

    new_user = User(id=None, name=full_name, email=email, password=password)
    user_repo.create(new_user)

    return redirect(url_for("get_index"))


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
    if "user_id" not in session:
        # Store the current URL in the session
        session["redirect_url"] = request.url
        return render_template("login.html")
    else:
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

        # In the booking_request route
        error_message = session.pop(
            "error_message", None
        )  # Retrieve and remove the error message from the session

        # Pass the error_message to the template
        return render_template(
            "rooms/room_book.html",
            room=room,
            min_date=min_date,
            booked_dates=booked_dates_dic,
            form=form,
            error_message=error_message,
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

            # Check if any dates in the selected range are already booked
            current_date = start_date
            while current_date <= end_date:
                if calendar_repo.is_date_booked(room_id, current_date):
                    error_message = "Dates already booked."
                    session[
                        "error_message"
                    ] = error_message  # Store the error message in the session
                    return redirect(url_for("booking_request", id=room_id))

                current_date += timedelta(days=1)

            # All dates in the range are available, add the booking to the database
            calendar_repo.add_booked_date(user_id, room_id, False, start_date, end_date)
            session["booking_complete"] = True
            flash("Booking was successful!", "success")
            return redirect(url_for("get_rooms"))

        else:
            # Handle the case where the user is not logged in
            # You can display an error message or redirect to the login page
            return redirect(url_for("login"))


@app.route("/rooms/room_new")
def get_new_room():
    return render_template("rooms/room_new.html")


@app.route("/rooms", methods=["POST"])
def create_new_room():
    connection = get_flask_database_connection(app)
    repo = RoomsRepository(connection)

    name = request.form["name"]
    price = int(request.form["price"])
    description = request.form["description"]

    room = Rooms(None, name, price, description, 1)

    repo.create(room)
    return redirect(f"/rooms")


@app.route("/index", methods=["GET"])
@app.route("/")
def get_index():
    return render_template("index.html")


# LOGIN
@app.route("/login")
def login():
    if "user_id" not in session:
        return render_template("login.html")
    else:
        return redirect(url_for("get_rooms"))


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
            session["user_id"] = user.id

            # Check if a redirect URL is stored in the session
            redirect_url = session.pop("redirect_url", None)
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect(url_for("get_rooms"))
        else:
            errors.append("Invalid login details.")

    return render_template("login.html", error_message=" ".join(errors))


@app.route("/logout")
def logout():
    # Clear the user's session
    session.clear()
    return redirect(url_for("login"))


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

    page = int(request.args.get("page", 1))
    per_page = 8
    offset = (page - 1) * per_page
    rooms = repo.get_rooms_paginated(offset, per_page)

    total_rooms = repo.get_total_rooms_count()
    has_next = (offset + per_page) < total_rooms

    return render_template(
        "rooms/room_index.html", rooms=rooms, page=page, has_next=has_next
    )


@app.route("/rooms/<id>", methods=["GET"])
def get_single_room(id):
    connection = get_flask_database_connection(app)
    room_repo = RoomsRepository(connection)
    room = room_repo.find(id)

    session["room_id"] = room.id

    booking_request_url = url_for("booking_request", id=id)

    return render_template(
        "rooms/room_show.html",
        room=room,
        booking_request_url=booking_request_url,  # Pass the URL to the template
    )


# BOOKINGS
@app.route("/bookings/<booking_id>", methods=["GET"])
def get_room_name_and_description_and_other_requests(booking_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking = booking_repository.find_with_room(booking_id)
    user = booking_repository.find_with_user(booking_id)
    bookings = booking_repository.find_all_bookings_for_this_room(booking_id)
    number_of_bookings = booking_repository.count_bookings_for_this_user(booking_id)
    return render_template(
        "bookings/show.html",
        booking=booking,
        user=user,
        bookings=bookings,
        number_of_bookings=number_of_bookings,
        booking_id=booking_id,
    )


@app.route("/bookings/<booking_id>/confirm", methods=["POST"])
def post_confirm_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking_repository.confirm_booking(booking_id)
    booking = booking_repository.find_with_room(booking_id)[0]
    return redirect(
        url_for(
            "get_room_name_and_description_and_other_requests", booking_id=booking.id
        )
    )


@app.route("/bookings/<booking_id>/deny", methods=["POST"])
def delete_deny_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking_repository.deny_booking(booking_id)
    # return render_template("rooms/room_index.html", rooms=rooms)
    return redirect(url_for("get_rooms", booking_id=booking_id))


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
