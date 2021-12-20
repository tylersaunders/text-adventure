import logging
import os
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
from server.engine.adventure_engine import AdventureEngine
from server.enums import Sockets

socket = SocketIO(logger=False, engineio_logger=False)


def create_app():

    app = Flask(
        __name__,
        static_url_path='',
        static_folder=os.path.abspath("../textadventure/web/"),
        template_folder=os.path.abspath("../textadventure/web/"),
    )
    app.config.from_mapping(SECRET_KEY='text-adventure', )

    socket.init_app(app)

    @socket.on(Sockets.CONNECT.value)
    def socket_connected():
        logging.debug('NEW PLAYER CONNECTED.')

    @socket.on(Sockets.START_GAME.value)
    def socket_start_game():
        logging.debug('NEW GAME REQUESTED BY PLAYER')
        AdventureEngine(socketio=socket,
                        scenario_path='./scenarios/christmas2021.yaml')

    @socket.on("connect_error")
    def socket_connect_error():
        logging.debug("error")

    @socket.on(Sockets.LOAD_GAME.value)
    def socket_load_game(game_id: str):
        logging.debug('LOAD GAME {} REQUESTED'.format(game_id))
        AdventureEngine(socketio=socket, game_id=game_id)

    @app.route('/')
    def index(**_):
        return render_template('index.html')

    return app
