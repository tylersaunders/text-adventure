import json
import logging
import uuid
from server.engine.location import Location
from server.engine.object import AdventureObject


class Scenario():
    """A text adventure scenario."""
    def __init__(self, title: str, greeting: str, starting_location_id: str,
                 **kwargs):
        self.title = title
        self.greeting = greeting
        self.starting_location_id = starting_location_id
        self.UNKNOWN_ACTION_RESPONSE = kwargs.get(
            'UNKNOWN_ACTION_RESPONSE', 'You aren\'t so sure about that.')
        self.game_id = kwargs.get('game_id', uuid.uuid4().__str__())
        self.all_locations = {}
        self.all_objects = {}
        self.player_location = None

    def add_location(self, loc: Location) -> None:
        """Register a location in the scenario

        Args:
            loc: The location to register.
            NOTE: The location must have a unique id inside of the scenario.
        """
        if self.all_locations.get(loc.id) is not None:
            raise RuntimeError('location already exists in scenario')
        else:
            self.all_locations[loc.id] = loc

    def add_object(self, obj: AdventureObject) -> None:
        """Register a location in the scenario

        Args:
            loc: The location to register.
            NOTE: The location must have a unique id inside of the scenario.
        """
        if self.all_objects.get(obj.id) is not None:
            raise RuntimeError('location already exists in scenario')
        else:
            self.all_objects[obj.id] = obj

    def begin(self) -> None:
        logging.debug('SCENARIO CONFIGURATION:')
        logging.debug(
            'all_locations: %s',
            [location.id for location in self.all_locations.values()])
        logging.debug('all_objects: %s',
                      [obj.id for obj in self.all_objects.values()])
        if not self.all_locations.get(self.starting_location_id):
            raise RuntimeError('staring location not found in all_locations')
        self.player_location = self.all_locations[self.starting_location_id]

    def move(self, direction: str):
        if direction in self.player_location.exits:
            self.player_location = self.all_locations[
                self.player_location.exits[direction]]
            return (self.player_location.look(), f'You travel {direction}.')
        else:
            return (None, 'You cannot go that way.')

    def serialize(self) -> str:
        """Transform the current scenario into a data string for storage."""
        data = {}
        data['game_id'] = self.game_id
        data['title'] = self.title
        data['greeting'] = self.greeting
        data['starting_location_id'] = self.starting_location_id
        data['UNKNOWN_ACTION_RESPONSE'] = self.UNKNOWN_ACTION_RESPONSE
        data['all_locations'] = [
            location.serialize() for location in self.all_locations.values()
        ]
        data['all_objects'] = [
            obj.serialize() for obj in self.all_objects.values()
        ]
        data['player_location'] = self.player_location.serialize(
        ) if self.player_location else ''
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data: str):
        """Transform a data string into a loaded scenario."""
        loaded = json.loads(data)
        scenario = cls(**loaded)
        for obj in loaded['all_objects']:
            loaded_obj = AdventureObject.deserialize(obj)
            scenario.all_objects[loaded_obj.id] = loaded_obj
        for loc in loaded['all_locations']:
            loaded_loc = Location.deserialize(loc)
            scenario.all_locations[loaded_loc.id] = loaded_loc
        player_location = Location.deserialize(loaded['player_location'])
        if player_location.id not in scenario.all_locations.keys():
            raise RuntimeError(
                'Player location could not be found in loaded data!')
        scenario.player_location = scenario.all_locations[player_location.id]
        return scenario
