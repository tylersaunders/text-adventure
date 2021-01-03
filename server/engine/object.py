import json
from typing import Tuple


class AdventureObject(object):
    def __init__(self, id: str, name: str, description: str, **kwargs):
        self.object_type = 'adventure_object'
        self.id = id
        self.name = name
        self.description = description

    def look(self) -> Tuple[str, str]:
        return (self.description, None)

    def serialize(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, data: str):
        data = json.loads(data)
        if data['object_type'] == 'activateable':
            obj = Activateable(**data)
        else:
            obj = cls(**data)
        return obj


class Activateable(AdventureObject):
    def __init__(self, id: str, name: str, description: str, on_description,
                 off_description: str, **kwargs):
        super().__init__(id, name, description)
        self.active = False
        self.object_type = 'activateable'
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
