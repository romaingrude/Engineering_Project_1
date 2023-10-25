import os
from flask import Flask, request, render_template, request
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.rooms import Rooms
from lib.rooms_repository import RoomsRepository

app = Flask(__name__)


#   ; open http://localhost:5000/index

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    new_user = User(id=None, name=name, email=email, password=password)
    SQL = f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{password}');" 
    db = get_flask_database_connection(app)
    print(f"db name{db._database_name()}")
    db.execute(SQL)
    return "Registration Successful"


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
