
import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.rooms import Rooms
from lib.rooms_repository import RoomsRepository
import secrets
from lib.user import User


app = Flask(__name__)


#   ; open http://localhost:5000/index

@app.route('/register')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    user_repo = UserRepository(get_flask_database_connection(app))

    full_name = f"{first_name} {last_name}"

    existing_user = user_repo.find_by_email(email)

    if existing_user:
        return render_template('signup.html', email_error="An account with this email already exists.")

    if (
        len(password) < 8
        or not any(char.isdigit() for char in password)
        or not any(char in '!@#$%^&*' for char in password)
    ):
        return render_template('signup.html', password_error="Password does not meet the requirements.")
    
    new_user = User(id=None, name=full_name, email=email, password=password)
    user_repo.create(new_user)

    return redirect(url_for("get_index"))

# Generate a secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask app
app.secret_key = secret_key


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

    return render_template("rooms/room_show.html", room=room)


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
def get_index():
    return render_template("index.html")



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


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
