import logging
from typing import Dict, List, Tuple
from enum import Enum
from server.engine.scenario import Scenario


class Actions(Enum):
    UNKNOWN = 'unknown'
    DROP = 'drop'
    LOOK = 'look'
    MOVE = 'move'
    TAKE = 'take'
    TURN_ON = 'turn_on'
    TURN_OFF = 'turn_off'


def parse(message: str, scenario: Scenario) -> Tuple[Actions, object, Dict]:
    """Attempts to parse the player action into an action, target and arguments.

    Args:
        message - the incoming message from the player-action socket.
        scenario - the current scenario state.

    Returns - a Tuple of the parsed action, the target object,
              and a list of arguments.
    """
    prepositions = [
        'of', 'on', 'in', 'to', 'for', 'with', 'from', 'around', 'under',
        'over', 'out', 'off', 'down', 'at'
    ]
    kwargs = {
        'player_inventory': scenario.player_inventory,
        'player_location': scenario.player_location,
        'all_objects': scenario.all_objects,
    }

    message = message.lower()
    words = message.split()

    action, direction = _parse_moving(words)
    if action == Actions.MOVE:
        logging.debug('action_parse: movement detected, %s, %s, %s', action,
                      scenario, direction)
        return (action, scenario, {'direction': direction, **kwargs})

    if len(words) == 1:
        # Assume action is in the form of <verb> (e.g. look, jump).
        verb = words[0]
        action = _parse_action(verb)
        logging.debug(
            'action_parse: single command, calling on current location.'
            '%s, %s', action, scenario.player_location)
        return (action, scenario.player_location, {**kwargs})

    if len(words) == 2:
        # Assume action is in the form <verb noun> (e.g. get lamp)
        verb, noun = words
        target = _parse_noun(scenario, noun)
        action = _parse_action(verb)
        # if no target was found, but the current location
        # can accept the action, call the action on the location.
        if not target and hasattr(scenario.player_location, action.value):
            logging.debug(
                'action_parse: target cannot accept action, but location can.'
                ' %s. %s', action, target, scenario.player_location)
            return (action, scenario.player_location, {**kwargs})

        logging.debug('action_parse: target can accept action, %s. %s', action,
                      target)
        return (action, target, {**kwargs})

    if len(words) == 3:
        # Assume action is in the form <verb adjective noun>
        # (e.g. get large key)
        # Or in the form <verb preposition noun>
        verb, two, noun = words
        if two in prepositions:
            target = _parse_noun(scenario, noun)
            action = _parse_action(verb, two)
            logging.debug('action_parse: target and action found, %s. %s',
                          action, target)
            return (action, target, {**kwargs})
        action = _parse_action(verb)
        target = _parse_noun(scenario, noun, two)
        logging.debug(
            'action_parse: target found, but unable to parse unknown action. '
            '%s, %s', action, target)
        if action is not Actions.UNKNOWN:
            return (action, target, {**kwargs})
        return (Actions.UNKNOWN, target, None)

    if len(words) == 4:
        # Assume action is in the form <verb preposition adjective noun>
        # (e.g. stand on sturdy chair).
        # or in the form <verb preposition preposition noun>
        # or in the form <verb noun preposition noun>
        verb, two, three, noun = words
        if two in prepositions:
            verb, prep, adj, noun = words
            target = _parse_noun(scenario, noun, adj)
            action = _parse_action(verb, two)
            logging.debug('action_parse: target and action found, %s. %s',
                          action, target)
            return (action, target, {**kwargs})
        if three in prepositions:
            verb, noun, prep, noun2 = words
            target = _parse_noun(scenario, noun)
            destination = _parse_noun(scenario, noun2)
            action = _parse_action(verb, prep)
            logging.debug('action_parse: target and action found, %s. %s',
                          action, target.id)
            return (action, target, {'destination': destination, **kwargs})
        else:
            logging.debug('action_parse: unable to parse unknown action.')
            return (Actions.UNKNOWN, None, {**kwargs})

    # If it gets this far, then we're not sure what to do.
    return (Actions.UNKNOWN, None, {**kwargs})


def _parse_action(verb: str, preposition: str = None) -> Actions:
    for action in Actions:
        if action.value == verb:
            return action
        elif preposition and action.value == f'{verb}_{preposition}':
            return action
    return Actions.UNKNOWN


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


def _parse_noun(scenario: Scenario,
                noun: str,
                adj: str = None) -> object or None:

    # Get the object references for all objects in the current
    # player location.
    relevant_objs = [
        obj for obj in scenario.all_objects.values()
        if obj.id in scenario.player_location.objects
    ]
    # Include the items the player is currently carrying.
    relevant_objs += [obj for obj in scenario.player_inventory.values()]

    # Get the names of those objects.
    all_named_objs = [obj.name for obj in relevant_objs if obj.name]

    # if there is only one match for the object, we're done!
    if all_named_objs.count(noun) == 1:
        index = all_named_objs.index(noun)
        return relevant_objs[index]

    if adj:
        adj_in_object = [
            obj for obj in relevant_objs
            if noun in obj.name and adj in str(obj)
        ]
        if len(adj_in_object) == 1:
            return adj_in_object[0]

    # Not specific enough, or we couldn't find the object.
    return None
