from typing import Tuple
from enum import Enum
from server.engine.location import Location


class Actions(Enum):
    UNKNOWN = 'unknown'
    LOOK = 'look'


def parse_user_input(message: str,
                     player_location: Location) -> Tuple[Actions, Location]:

    action = _parse_action(message)
    target = _parse_action_target(message, player_location)
    return (action, target)


def _parse_action(message: str) -> Actions:

    message = message.lower()
    message = message.split()

    if len(message) == 1:
        verb = message[0]
        for action in Actions:
            if verb == action.value:
                return action

    return Actions.UNKNOWN


def _parse_action_target(message: str, player_location) -> Location:
    print(player_location)
    return player_location
