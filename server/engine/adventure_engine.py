from server.engine.scenario import Scenario
from flask_socketio import SocketIO, emit
from server.engine.actions import parse_user_input, Actions
from server.enums import Sockets


class AdventureEngine():
    """A Text Adventure engine."""
    def __init__(self, socketio: SocketIO, scenario: Scenario = None):
        """Create a new adventure.

        Args:
            data: serialized game data. If provided, calls self.deserialize to
                restore game state.
        """
        self.socket = socketio
        self.scenario = scenario
        emit('adventure-text', self.scenario.greeting)

        @self.socket.on(Sockets.PLAYER_ACTIONS.value)
        def handle_user_action(action):
            """Listens for user-action messages and forwards them to act."""
            self.act(action)

    def __eq__(self, other) -> bool:
        """Compares two text adventure instances for equality"""
        return False

    def __ne__(self, other) -> bool:
        """Compares to text adventure instances for inequality"""
        return True

    def deserialize(data) -> None:
        """Restore the adventure state."""
        pass

    def serialize(self) -> str:
        """Save the current adventure state."""
        pass

    def act(self, action) -> None:
        """Takes an action and attempts to call it on the adventure instance.

        Args:
            action: the unparsed player's action from the websocket.
        """
        action, target = parse_user_input(action,
                                          self.scenario.player_location)

        if action == Actions.UNKNOWN:
            emit(Sockets.ACTION_TEXT.value,
                 self.scenario.UNKNOWN_ACTION_RESPONSE)
            return

        emit(Sockets.ACTION_TEXT.value, f'Your action was {action.value}')