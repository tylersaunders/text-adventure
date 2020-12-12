"""Location classes for text-adventure."""
from typing import List, Tuple
from server.engine.object import AdventureObject


class Location(object):
    """A location in a scenario. (Such as a room or place)."""
    objects: List[AdventureObject]

    def __init__(self, description: str) -> None:
        self.description = description
        self.exits = {}
        self.objects = []

    def look(self) -> Tuple[str, str]:
        return self.description, 'You look around.'
