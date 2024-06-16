import os

import socketio
import eventlet.wsgi
from dotenv import load_dotenv
load_dotenv()

sio = socketio.Server(cors_allowed_origins="*")

appSocket = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(f"Client connecté : {sid}")


@sio.event
def disconnect(sid):
    print(f"Client déconnecté : {sid}")


@sio.event
def task_done(sid, result):
    channel = result['id']
    data = result['content']
    sio.emit(channel, data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((os.getenv('SERVER_SOCKET_HOST'), int(os.getenv('SERVER_SOCKET_PORT')))), appSocket)
