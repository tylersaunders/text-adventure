from typing import Tuple, Optional
from server.engine.location import Location


class AdventureObject(object):
    def __init__(self,
                 id: str,
                 name: str,
                 description: str,
                 takeable: Optional[bool] = False):
        self.id = id
        self.name = name
        self.description = description
        self.takeable = takeable

    def look(self, **kwargs) -> Tuple[str, str]:
        return (self.description, None)

    def take(self, player_inventory: object, player_location: Location,
             **kwargs):
        if self.takeable and self.id not in player_inventory:
            player_location.objects.remove(self.id)
            player_inventory[self.id] = self
            return None, f'You take the {self.name}.'
        elif self.id in player_inventory:
            return None, f'You are already carrying the {self.name}.'
        else:
            return None, 'You can\'t take that.'

    def drop(self, player_inventory: object, player_location: Location,
             **kwargs):
        if self.takeable and self.id in player_inventory:
            player_location.objects.append(self.id)
            del player_inventory[self.id]
            return None, f'You drop the {self.name}.'
        elif self.id not in player_inventory:
            return None, f'You aren\'t carrying a {self.name}.'
        else:
            return None, f'This isn\'t a good place to drop the {self.name}.'


class Activateable(AdventureObject):
    active = False

    def __init__(self,
                 id: str,
                 name: str,
                 description: str,
                 on_description,
                 off_description: str,
                 takeable: Optional[bool] = False):
        super().__init__(id, name, description)
        self.on_description = on_description
        self.off_description = off_description

    def turn_on(self, **kwargs) -> Tuple[str, str]:
        if self.active is True:
            return (None, f'The {self.name} is already on.')
        self.active = True
        return (self.on_description, f'You turn on the {self.name}.')

    def turn_off(self, **kwargs) -> Tuple[str, str]:
        if self.active is False:
            return (None, f'The {self.name} is already off.')
        self.active = False
        return (self.off_description, f'You turn off the {self.name}.')

    def look(self, **kwargs) -> Tuple[str, str]:
        if self.active:
            return (self.on_description,
                    f'You take a closer look at the {self.name}.')
        else:
            return (self.off_description,
                    f'You take a closer look at the {self.name}.')
