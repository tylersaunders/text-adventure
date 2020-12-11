"""Location classes for text-adventure."""
from typing import Tuple, List


class Location(object):
    """A location in a scenario. (Such as a room or place)."""
    description: str = None
    exits = {}

    def __init__(self, description: str) -> None:
        self.description = description

    def look(self) -> Tuple[str, str]:
        return self.description, 'You look around.'
