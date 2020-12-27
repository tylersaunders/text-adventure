"""Location classes for text-adventure."""
from typing import List, Tuple


class Location(object):
    """A location in a scenario. (Such as a room or place)."""
    id: str = ''
    objects: List[str]

    def __init__(self, id: str, description: str) -> None:
        self.id = id
        self.description = description
        self.exits = {}
        self.objects = []

    def look(self, all_objects: object, **kwargs) -> Tuple[str, str]:
        return self.description, 'You look around.'
