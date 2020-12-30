import logging
from flask_socketio import SocketIO, emit
from server.engine.actions import parse, Actions
from server.enums import Sockets
from server.engine.scenario_parser import load_scenario


class AdventureEngine():
    """A Text Adventure engine."""
    def __init__(self, socketio: SocketIO, scenario_path: str):
        """Create a new adventure.

        Args:
            data: serialized game data. If provided, calls self.deserialize to
                restore game state.
        """
        self.socket = socketio
        logging.debug("PARSING SCENARIO")
        self.scenario = load_scenario(scenario_path)
        logging.debug(self.scenario)
        self.scenario.begin()
        emit(Sockets.ADVENTURE_TITLE.value, self.scenario.title)
        emit(Sockets.ADVENTURE_TEXT.value, self.scenario.greeting)
        emit(Sockets.ACTION_TEXT.value, None)
        emit(
            Sockets.INVENTORY.value, ','.join([
                item.name for item in self.scenario.player_inventory.values()
            ]))

        @self.socket.on(Sockets.PLAYER_ACTIONS.value)
        def handle_user_action(action):
            """Listens for user-action messages and forwards them to act."""
            logging.debug(
                'ADVENTURE_ENGINE: incoming player action: {}'.format(action))
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
        # Parse the incoming action, target and arguments.
        action, target, kwargs = parse(action, self.scenario)

        # If the action isn't understood, return the scenario's
        # default unknown action.
        if action == Actions.UNKNOWN:
            emit(Sockets.ACTION_TEXT.value,
                 self.scenario.UNKNOWN_ACTION_RESPONSE)
            return

        # try to call the action on the target with the parsed args.
        try:
            action_result = getattr(target, action.value)(**kwargs)
            logging.debug(action_result)
        except AttributeError:
            logging.exception('Attribute {} not found on {}'.format(
                action.value, target))
            # the target doesn't accept that action, so return unknown action
            # to the user.
            emit(Sockets.ACTION_TEXT.value,
                 self.scenario.UNKNOWN_ACTION_RESPONSE)
            return

        if action_result.adventure_text:
            emit(Sockets.ADVENTURE_TEXT.value, action_result.adventure_text)
        if action_result.action_text:
            emit(Sockets.ACTION_TEXT.value, action_result.action_text)
        if action_result.push_inventory_update:
            item_names = [
                item.name for item in self.scenario.player_inventory.values()
            ]
            emit('inventory', ','.join(item_names))
