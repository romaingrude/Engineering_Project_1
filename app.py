import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from lib.rooms import Rooms
from lib.rooms_repository import RoomsRepository

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
