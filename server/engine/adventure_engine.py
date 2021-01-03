import logging
import os
from flask_socketio import SocketIO, emit
from server.engine.actions import parse, Actions
from server.enums import Sockets
from server.engine.scenario_parser import load_scenario
from server.engine.scenario import Scenario
from typing import Optional


class AdventureEngine():
    """A Text Adventure engine."""
    def __init__(self,
                 socketio: SocketIO,
                 scenario_path: Optional[str] = None,
                 game_id: Optional[str] = None):
        """Create a new adventure.

        Args:
            data: serialized game data. If provided, calls self.deserialize to
                restore game state.
        """
        self.socket = socketio
        if scenario_path:
            logging.debug("PARSING SCENARIO")
            self.scenario = load_scenario(scenario_path)
            logging.debug(self.scenario)
            self.scenario.begin()
            emit(Sockets.ADVENTURE_TITLE.value, self.scenario.title)
            emit(Sockets.ADVENTURE_TEXT.value, self.scenario.greeting)
            emit(Sockets.ACTION_TEXT.value, None)
            emit(Sockets.GAME_ID.value, self.scenario.game_id)
            emit(
                Sockets.INVENTORY.value, ','.join([
                    item.name
                    for item in self.scenario.player_inventory.values()
                ]))
            self.serialize()
        elif game_id:
            logging.debug("Resuming game id {}".format(game_id))
            self.scenario = self.deserialize(game_id)
            emit(Sockets.ADVENTURE_TITLE.value, self.scenario.title)
            emit(
                Sockets.ADVENTURE_TEXT.value,
                self.scenario.player_location.look(
                    all_objects=self.scenario.all_objects).adventure_text)
            emit(
                Sockets.INVENTORY.value, ','.join([
                    item.name
                    for item in self.scenario.player_inventory.values()
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

    def deserialize(self, game_id: str) -> Scenario:
        """Restore the adventure state."""
        if not os.path.exists(f'games'):
            raise RuntimeError('No games directory found.')
        try:
            with open(f"./games/{game_id}", "r") as saved_game:
                data = saved_game.read()
                saved_game.close()
        except IOError:
            logging.exception('Requested game data does not exist.')
        print(data)
        return Scenario.deserialize(data)

    def serialize(self) -> None:
        """Save the current adventure state."""
        if not os.path.exists('games'):
            os.makedirs('games')
        with open(f'./games/{self.scenario.game_id}', "w+") as save_game:
            save_game.write(self.scenario.serialize())
            save_game.close()

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
            emit(Sockets.INVENTORY.value, ','.join(item_names))
        self.serialize()
