from typing import Tuple


class AdventureObject(object):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def look(self) -> Tuple[str, str]:
        return (self.description, None)


class Activateable(AdventureObject):
    active = False

    def __init__(self, name: str, description: str, on_description,
                 off_description: str):
        super().__init__(name, description)
        self.on_description = on_description
        self.off_description = off_description

    def turn_on(self) -> Tuple[str, str]:
        if self.active is True:
            return (None, f'The {self.name} is already on.')
        self.active = True
        return (self.on_description, f'You turn on the {self.name}.')

    def turn_off(self) -> Tuple[str, str]:
        if self.active is False:
            return (None, f'The {self.name} is already off.')
        self.active = False
        return (self.off_description, f'You turn off the {self.name}.')

    def look(self) -> Tuple[str, str]:
        if self.active:
            return (self.on_description,
                    f'You take a closer look at the {self.name}.')
        else:
            return (self.off_description,
                    f'You take a closer look at the {self.name}.')
