"""Location classes for text-adventure."""
from typing import List, Tuple
import json


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

    def look(self) -> Tuple[str, str]:
        return self.description, 'You look around.'
