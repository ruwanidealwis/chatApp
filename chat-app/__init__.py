from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, join_room
app = Flask(__name__)
username_dict = {}
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        jsonData = request.json
        print(jsonData)
        username = jsonData['username']
        print("redirecting....")
        return redirect(url_for('chat', username=username), code=302)
    else:
        return render_template('main.html')


@ app.route('/chat/<room_id>')
def load_room(room_id=0):
    print(room_id)
    # get messages from db
    return render_template('chat_room.html',  username="x")


@ app.route('/chat', methods=["GET"])
def chat():
    return render_template('chat.html', username=request.args.get('username'))


@ socketio.on('connected')
def connected_users(json, methods=['GET', 'POST']):
    username_dict[json["socketID"]] = json["username"]
    print('received a new user: ' + str(json))
    socketio.emit('new active user', json)


@ socketio.on('message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    # TODO save messages to database
    print('received my message: ' + str(json))
    if json["roomName"]:
        route = '/chat/' + json["roomName"]
        socketio.emit('my response', json,
                      room=json["roomName"])
    else:
        socketio.emit('my response', json)


@socketio.on('join room')
def join_new_room(data):
    join_room(data["roomName"])
    print(data)
    route = '/chat/' + data["roomName"]
    # let client know room was created
    # get previous message history...
    socketio.emit("joined room", data,
                  room=data["roomName"])

# guest recieves an invite to join the room


@socketio.on('send invite')
def send_invite(data):
    print(data)
    data["username"] = username_dict[data["userID"]]
    # send an invite to guest...
    socketio.emit("accept invite", data, room=data["userID"])


@socketio.on('add to room')
def add_to_room(data):
    # now joib room, after accepting invite
    join_room("x's room")
    socketio.emit("joined room", "Connected a new user to x's room",
                  room="x's room")


if __name__ == "__main__":
    socketio.run(app)
