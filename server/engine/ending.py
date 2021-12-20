import json
import logging


class Ending(object):
    """An ending to a game in text-adventure."""
    def __init__(self, **kwargs):
        self.location_id = kwargs.get('location_id', None)
        self.message = kwargs.get('message', None)
        self.requires = kwargs.get('requires', [])

    @classmethod
    def parse(cls, **kwargs):
        return cls(**kwargs)

    def fulfilled(self, player_inventory: dict,
                  player_location_id: str) -> bool:
        """Returns whether an ending is fullfilled by the scenario state."""
        if player_location_id == self.location_id:
            for item_id in self.requires:
                if not item_id in player_inventory.keys():
                    return False
        else:
            return False

        # If we make it this far, the player is in the ending location and
        # has all items required to end the game with this ending.
        return True

    def serialize(self):
        """Stores the ending for saving to a game file."""
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, data: str):
        """Rehydrates the ending from a data string."""
        data = json.loads(data)
        return cls(**data)
