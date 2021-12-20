"""Location classes for text-adventure."""
from typing import List, Tuple
import json
from server.engine.action_result import ActionResult


class Location(object):
    """A location in a scenario. (Such as a room or place)."""
    id: str = ''
    objects: List[str]

    def __init__(self, id: str, description: str, **kwargs) -> None:
        self.id = id
        self.description = description

        self.exits = {}
        for exit, location_id in kwargs.get('exits', {}).items():
            self.exits[exit] = location_id

        self.objects = kwargs.get('objects', [])
        self.requires = kwargs.get('requires', [])
        self.travel_action = kwargs.get('travel_action', None)
        self.travel_failure = kwargs.get('travel_failure', None)

    def __repr__(self):
        return f'{self.id}'

    def serialize(self) -> str:
        return json.dumps(self.__dict__)

    def remove_requirement(self, item_id):
        self.requires.remove(item_id)

    @classmethod
    def deserialize(cls, data: str):
        loaded_data = json.loads(data)
        location = cls(loaded_data['id'], loaded_data['description'])
        location.exits = loaded_data['exits']
        location.objects = loaded_data['objects']
        location.requires = loaded_data['requires']
        location.travel_failure = loaded_data['travel_failure']
        location.travel_action = loaded_data['travel_action']
        return location

    def look(self, all_objects: object, **kwargs) -> Tuple[str, str]:
        adventure_text = self.description

        # Add description for any objects on the ground.
        for obj_id in self.objects:
            obj = all_objects[obj_id]
            if obj and obj.location_description:
                adventure_text += " "
                adventure_text += obj.location_description
        return ActionResult(adventure_text=adventure_text,
                            action_text='You look around.')
