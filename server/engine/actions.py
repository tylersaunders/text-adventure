from typing import Tuple, List
from enum import Enum
from server.engine.scenario import Scenario


class Actions(Enum):
    UNKNOWN = 'unknown'
    LOOK = 'look'
    MOVE = 'move'


def parse(message: str, scenario: Scenario) -> Tuple[Actions, object, List]:
    """Attempts to parse the player action into an action, target and arguments.

    Args:
        message - the incoming message from the player-action socket.
        scenario - the current scenario state.

    Returns - a Tuple of the parsed action, the target object,
              and a list of arguments.
    """

    message = message.lower()
    words = message.split()

    if len(words) == 1:
        # Assume action is in the form of <verb> (e.g. look, jump).

        action, direction = _parse_moving(words)
        if action == Actions.MOVE:
            return (action, scenario, [direction])

        verb = words[0]
        for action in Actions:
            if action.value == verb:
                return (action, scenario.player_location, [])

        return (Actions.UNKNOWN, None, None)

    if len(words) == 2:
        # Assume action is in the form <verb noun> (e.g. get lamp)
        pass

    if len(words == 3):
        # Assume action is in the form <verb adjective noun>
        # (e.g. get large key)
        pass

    if len(words == 4):
        # Assume action is in the form <verb preposition adjective noun>
        # (e.g. stand on sturdy chair).
        pass


def _parse_moving(message: List[str]) -> Tuple[Actions, str]:
    """Parses the incoming message list to determine if movement is found.

    Args:
        message: list of words in the player message

    Returns: a tuple of the action and direction
    """

    short_dir = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    long_dir = [
        'north', 'northeast', 'east', 'southeast', 'south', 'southwest',
        'west', 'northwest'
    ]

    for d in long_dir:
        if d in message:
            return (Actions.MOVE, d)
    for d in short_dir:
        if d in message:
            direction = long_dir[short_dir.index(d)]
            return (Actions.MOVE, direction)

    return (Actions.UNKNOWN, '')
