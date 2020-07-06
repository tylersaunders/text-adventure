# python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

socketio = SocketIO()


def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='../build',
                template_folder='../build/')

    @app.route('/')
    def index(**_):
        return render_template('index.html')

    socketio.init_app(app)

    @socketio.on('connect')
    def connect():
        """When a client connects, this should start the adventure."""
        greeting = (
            'Thunder cracks as the rain comes down in the night. Out '
            'the window, the world is dark, black. You can\'t see the '
            'rain, but you can hear it as the chill of winter runs down '
            'your spine. In the corner, a dying fire is the only source '
            'of warmth in this frigid place.')
        emit('adventure-text', greeting)
        pass

    @socketio.on('user-action')
    def message(message):
        """When receiving action text from the user."""
        emit('adventure-text', 'one dark night')
        emit('action-text', f"You {message}")

    return app
