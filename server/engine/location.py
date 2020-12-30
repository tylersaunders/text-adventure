"""Location classes for text-adventure."""
from typing import List, Tuple
from server.engine.action_result import ActionResult


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
        return ActionResult(adventure_text=self.description,
                            action_text='You look around.')
