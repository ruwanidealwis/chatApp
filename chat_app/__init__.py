from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, join_room
app = Flask(__name__)
username_dict = {}
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['POST', 'GET'])
def entry():
    """entry point for flask application

    Returns:
        [html]: returns the main HTML template if GET, redirects to /chat if POST
    """
    if request.method == 'POST':
        jsonData = request.json
        print(jsonData)
        username = jsonData['username']
        print("redirecting....")
        return redirect(url_for('chat', username=username), code=302)
    else:
        return render_template('main.html')


@ app.route('/chat', methods=["GET"])
def chat():
    """  the chat view after the user logs in
    Args:
        methods (list, optional): [Type of HTTP request]. Defaults to ['GET', 'POST'].
    Returns:
        [HTML template]: [load chat view]
    """
    return render_template('chat.html', username=request.args.get('username'))


@ socketio.on('connected')
def connected_users(data, methods=['GET', 'POST']):
    """[when a new user connects to a client]

    Args:
        data ([json]): information about the new user (ie: username)
        methods (list, optional): HTTP methods. Defaults to ['GET', 'POST'].
    """
    username_dict[data["socketID"]] = data["username"]
    print('received a new user: ' + str(data))
    socketio.emit('new active user', data)


@ socketio.on('message')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    """ when server recieves a message event

    Args:
        data ([jaon]): information about message, (message, room name)
        methods (list, optional):  HTTP methods.. Defaults to ['GET', 'POST'].
    """
    # TODO save messages to database
    print('received my message: ' + str(data))

    if "roomName" in data:
        route = '/chat/' + data["roomName"]
        socketio.emit('my response', data,
                      room=data["roomName"])

    else:

        socketio.emit('my response', data)


@socketio.on('join room')
def join_new_room(data):
    """joins a chat room (ie: private messaging groups)

    Args:
        data (json): information about the room (ie: room name, user)
    """
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
    """sends an invite event to invite a user to room

    Args:
        data (json): information related to the invite (ie: room name, user ID)
    """
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
