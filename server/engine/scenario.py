import logging
from dataclasses import replace
from server.engine.location import Location
from server.engine.object import AdventureObject
from server.engine.action_result import ActionResult


class Scenario():
    """A text adventure scenario."""

    title: str = ''
    greeting: str = ''
    UNKNOWN_ACTION_RESPONSE: str = 'You aren\'t so sure about that.'
    all_locations = {}
    all_objects = {}
    player_location: Location = None
    player_inventory = {}

    def __init__(self, title: str, greeting: str, starting_location_id: str):
        self.title = title
        self.greeting = greeting
        self.starting_location_id = starting_location_id

    def add_location(self, loc: Location) -> None:
        """Register a location in the scenario.

        Args:
            loc: The location to register.
            NOTE: The location must have a unique id inside of the scenario.
        """
        if self.all_locations.get(loc.id) is not None:
            raise RuntimeError('location already exists in scenario')
        else:
            self.all_locations[loc.id] = loc

    def add_object(self, obj: AdventureObject) -> None:
        """Register a location in the scenario.

        Args:
            loc: The location to register.
            NOTE: The location must have a unique id inside of the scenario.
        """
        if self.all_objects.get(obj.id) is not None:
            raise RuntimeError('location already exists in scenario')
        else:
            self.all_objects[obj.id] = obj

    def begin(self) -> None:
        """Begins the scenario.
        The initialization logic once a Scenario is fully assembled and the
        AdventureEngine is ready to send the first message to the player.
        """
        logging.debug('SCENARIO CONFIGURATION:')
        logging.debug(
            'all_locations: %s',
            [location.id for location in self.all_locations.values()])
        logging.debug('all_objects: %s',
                      [obj.id for obj in self.all_objects.values()])
        if not self.all_locations.get(self.starting_location_id):
            raise RuntimeError('staring location not found in all_locations')
        self.player_location = self.all_locations[self.starting_location_id]

    def move(self, direction: str, **kwargs):
        """Move action handler for the scenario.
        NOTE: This is the only handler that is called on a MOVE action.
        """
        if direction in self.player_location.exits:
            self.player_location = self.all_locations[
                self.player_location.exits[direction]]
            return replace(self.player_location.look(kwargs),
                           action_text=f'You travel {direction}.')
        else:
            return ActionResult(action_text='You cannot go that way.')
