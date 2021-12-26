import json
import logging
import uuid

from typing import Type, TypeVar

from dataclasses import replace
from server.engine.action_result import ActionResult
from server.engine.ending import Ending
from server.engine.location import Location
from server.engine.object import AdventureObject, Activateable

# Generic variable that can be 'Scenario' or any subclass.
T = TypeVar('T', bound='Scenario')


class Scenario():
    """A text adventure scenario."""
    def __init__(self, title: str, greeting: str, starting_location_id: str,
                 **kwargs):
        self.title: str = title
        self.greeting: str = greeting
        self.starting_location_id: str = starting_location_id
        self.UNKNOWN_ACTION_RESPONSE: str = kwargs.get(
            'UNKNOWN_ACTION_RESPONSE', 'You aren\'t so sure about that.')
        self.game_id: str = kwargs.get('game_id', uuid.uuid4().__str__())
        self.all_locations: Dict[str, Location] = {}
        self.all_objects: Dict[str, AdventureObject] = {}
        self.all_endings: list[Ending] = []
        self.player_inventory: Dict[str, AdventureObject] = {}
        self.player_location = None
        self.ended = False

    def __repr__(self):
        return f'{self.title}, locs: {self.all_locations} objs: {self.all_objects}, endings: {self.all_endings}'

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

    def add_ending(self, ending: Ending):
        self.all_endings.append(ending)

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

    def move(self, direction: str, **kwargs) -> ActionResult:
        """Move action handler for the scenario.
        NOTE: This is the only handler that is called on a MOVE action.
        """
        if direction in self.player_location.exits:

            target_loc = self.all_locations[
                self.player_location.exits[direction]]

            # Check to see if the location requires any items.
            if target_loc.requires:
                for item_id in target_loc.requires:
                    if item_id not in self.player_inventory:
                        return ActionResult(
                            action_text=target_loc.travel_failure)

            self.player_location = target_loc

            # After moving, remove any required items.
            for item_id in target_loc.requires:
                self.player_inventory.pop(item_id)
                target_loc.remove_requirement(item_id)

            # Check to see if the move ends the game.
            for ending in self.all_endings:
                if ending.fulfilled(self.player_inventory,
                                    self.player_location.id):
                    self.ended = True
                    return ActionResult(adventure_text=ending.message,
                                        action_text="")

            action_text = target_loc.travel_action or f'You travel {direction}.'

            # Use replace because look also returns a ActionResult.
            # (And we want the action_text to be either the generic travel text
            #  or the location custom travel_action.)
            return replace(self.player_location.look(**kwargs),
                           action_text=action_text,
                           push_inventory_update=True)
        else:
            return ActionResult(action_text='You cannot go that way.')

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
        data['player_inventory'] = [
            obj.serialize() for obj in self.player_inventory.values()
        ]
        data['all_endings'] = [
            ending.serialize() for ending in self.all_endings
        ]
        logging.debug(f'serialize scenario: {self}')
        return json.dumps(data)

    @classmethod
    def deserialize(cls: Type[T], data: str) -> T:
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
        for obj in loaded['player_inventory']:
            loaded_obj = AdventureObject.deserialize(obj)
            scenario.player_inventory[loaded_obj.id] = loaded_obj
        for ending in loaded['all_endings']:
            scenario.add_ending(Ending.deserialize(ending))
        logging.debug(f'deserialize scenario: {scenario}')
        return scenario
