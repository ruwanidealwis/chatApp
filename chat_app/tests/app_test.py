import pytest
from chat_app import app, socketio
from flask import url_for, request
import json


def test_connection():
    # start flask app
    client = app.test_client()

    # start socket io
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # is connected
    assert socketio_test_client.is_connected()

    # HTTP request
    response = client.post('/', data=json.dumps(dict(username='testUser')), content_type='application/json',
                           follow_redirects=True)
    assert response.status_code is 200
    # assert request.path == url_for('chat')
    assert b'Currently Active Users' in response.data

    socketio_test_client.emit(
        'connected', dict(username='testUser', socketID='234519023'))
    # make sure the server accepted the connection
    r = socketio_test_client.get_received()
    print(r)
    assert len(r) == 1
    # check if server emitted the correct event...
    assert r[0]['name'] == 'new active user'
    assert len(r[0]['args']) == 1
    assert r[0]['args'][0] == {'username': 'testUser', 'socketID': '234519023'}


def test_message():
    # start flask app
    client = app.test_client()

    # start socket io
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # is connected
    assert socketio_test_client.is_connected()

    # HTTP request
    response = client.get('/chat?username=testUser')

    # test without room name
    socketio_test_client.emit(
        'message', dict(username='testUser', message='hello!', socketID='234519023'))
    r = socketio_test_client.get_received()
    print(r)
    assert len(r) == 1

    # check if server emitted the correct event...
    assert r[0]['name'] == 'my response'
    assert len(r[0]['args']) == 1
    assert r[0]['args'][0] == {'username': 'testUser',
                               'socketID': '234519023', 'message': 'hello!'}


def test_join_room():
    # start flask app
    client = app.test_client()

    # start socket io
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # is connected
    assert socketio_test_client.is_connected()

    socketio_test_client.emit(
        'join room', dict(roomName='1234'))
    r = socketio_test_client.get_received()
    # check if server emitted the correct event...
    print(r)
    assert r[0]['name'] == 'joined room'
    assert len(r[0]['args']) == 1
    assert r[0]['args'][0] == {'roomName': '1234'}


def test_send_invite():
    # start flask app
    client = app.test_client()

    # start socket io
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # is connected
    assert socketio_test_client.is_connected()

    # user has to first connect
    socketio_test_client.emit(
        'connected', dict(username='testUser', socketID='234519023'))

    socketio_test_client.emit(
        'send invite', dict(userID='234519023'))
    r = socketio_test_client.get_received()
    # check if server emitted the correct event...
    print(r)


def test_messageToRoom():
    # start flask app
    client = app.test_client()

    # start socket io
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # is connected
    assert socketio_test_client.is_connected()

    # join room
    socketio_test_client.emit(
        'join room', dict(roomName='1234'))

    # test message with room name
    socketio_test_client.emit(
        'message', dict(username='testUser', message='hello!', socketID='234519023'))
    chatResponse = socketio_test_client.get_received()

    print(chatResponse)
    # one to join the room, one after sending the message
    assert len(chatResponse) == 2

    # check if server emitted the correct event...
    assert chatResponse[1]['name'] == 'my response'
    assert len(chatResponse[1]['args']) == 1
    assert chatResponse[1]['args'][0] == {'message': 'hello!',   'socketID': '234519023', 'username': 'testUser',
                                       }


'''


from chat_app import app, socketio
from flask import url_for, request
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # init db later
            pass
        yield client


def test_start(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'<!DOCTYPE html>' in rv.data


def test_login(client):
    response = client.post('/', data=json.dumps(dict(username='testUser')), content_type='application/json',
                           follow_redirects=True)
    assert request.path == url_for('chat')
    assert b'Currently Active Users' in response.data

    socketio_client = socketio.test_client(
        app)
    assert socketio_client.is_connected()

    recieved = socketio_client.get_received()

    assert recieved[0]['username'] == 'testUser'
    # assert len(recieved) == 1
# make sure the server rejected the connection

# check socketio connection...


def test_messages(client):

    response = client.get('/chat?username=testuser')
    socketio_client = socketio.test_client(
        app)
    assert socketio_client.is_connected()
    socketio_client.emit('message', "hello")
'''
