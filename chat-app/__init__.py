from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO
app = Flask(__name__)
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


@ app.route('/chat', methods=["GET"])
def chat():

    return render_template('chat.html', username=request.args.get('username'))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@ socketio.on('connected')
def connected_users(json, methods=['GET', 'POST']):
    print('received a new user: ' + str(json))
    socketio.emit('new active user', json, callback=messageReceived)


@ socketio.on('message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my message: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == "__main__":
    socketio.run(app)
