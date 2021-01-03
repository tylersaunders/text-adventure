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
        self.objects = []

    def serialize(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, data: str):
        loaded_data = json.loads(data)
        location = cls(loaded_data['id'], loaded_data['description'])
        location.exits = loaded_data['exits']
        location.objects = loaded_data['objects']
        return location

    def look(self, all_objects: object, **kwargs) -> Tuple[str, str]:
        return ActionResult(adventure_text=self.description,
                            action_text='You look around.')
