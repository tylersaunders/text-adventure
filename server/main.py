import logging
from flask import Flask, render_template
from flask_socketio import SocketIO
from server.engine.adventure_engine import AdventureEngine
from server.enums import Sockets

socket = SocketIO()


def create_app():
    app = Flask(
        __name__,
        static_url_path='',
        static_folder='../build',
        template_folder='../build/',
    )

    socket.init_app(app)
    logging.basicConfig(level=logging.DEBUG)

    @socket.on(Sockets.CONNECT.value)
    def socket_connected():
        AdventureEngine(socket, './scenarios/lynelle.yaml')

    @app.route('/')
    def index(**_):
        return render_template('index.html')

    return app
