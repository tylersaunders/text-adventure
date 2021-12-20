import json
import logging
from typing import Tuple
from server.engine.location import Location
from server.engine.action_result import ActionResult
from server.enums import ObjectTypes


class AdventureObject(object):
    """The default object class in text-adventure. All game objects
    should inherit from this base class which provides basic
    implementations for look, take and drop actions.

    Objects can only be picked up & dropped by the player if they are marked
    with takeable=True.
    """
    def __init__(self, id: str, name: str, description: str, **kwargs):
        self.object_type = 'adventure_object'
        self.id = id
        self.name = name
        self.description = description
        self.takeable = kwargs.get('takeable', False)
        self.location_description = kwargs.get('location_description', None)
        self.requires = kwargs.get('requires', [])
        self.take_failure = kwargs.get('take_failure', None)
        self.take_action = kwargs.get('take_action', None)

    def __repr__(self):
        return f'{self.id}: {self.name}'

    def look(self, **kwargs) -> ActionResult:
        """Look action handler for AdventureObject.
        Returns:
            An Action result.
        """
        return ActionResult(adventure_text=self.description)

    def take(self, player_inventory: object, player_location: Location,
             **kwargs) -> ActionResult:
        """Take action handler for AdventureObject.
        Returns:
            An Action result.
        """
        if self.takeable and self.id not in player_inventory:

            if self.requires:
                for item_id in self.requires:
                    if item_id not in player_inventory:
                        return ActionResult(action_text=self.take_failure)

            for item_id in self.requires:
                player_inventory.pop(item_id)
                self.requires.remove(item_id)

            logging.debug('Adding {} to user inventory'.format(self.id))
            player_location.objects.remove(self.id)
            player_inventory[self.id] = self
            action_text = self.take_action or f'You take the {self.name}.'
            return ActionResult(
                action_text=action_text,
                push_inventory_update=True,
            )
        elif self.id in player_inventory:
            return ActionResult(
                action_text=f'You are already carrying the {self.name}.')
        else:
            return ActionResult(action_text='You can\'t take that.')

    def drop(self, player_inventory: object, player_location: Location,
             **kwargs):
        """Drop action handler for AdventureObject.
        Returns:
            An Action result.
        """
        if self.takeable and self.id in player_inventory:
            logging.debug('Removing {} from user inventory'.format(self.id))
            player_location.objects.append(self.id)
            del player_inventory[self.id]
            return ActionResult(action_text=f'You drop the {self.name}.',
                                push_inventory_update=True)
        elif self.id not in player_inventory:
            return ActionResult(
                action_text=f'You aren\'t carrying a {self.name}.')
        else:
            return ActionResult(action_text=(
                f'This isn\'t a good place to drop the {self.name}.'))

    @classmethod
    def parse(cls, **kwargs):
        base_object = kwargs.get("base_object",
                                 ObjectTypes.ADVENTURE_OBJECT.value)
        if base_object == ObjectTypes.ACTIVATEABLE.value:
            obj = Activateable(**kwargs)
        else:
            obj = cls(**kwargs)

        return obj

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
    """An Activateable object that makes use of the TURN_ON and TURN_OFF actions.
    The look action is overriden here to provide the correct response based
    on the active status of the Activateable.
    """
    def __init__(
        self,
        id: str,
        name: str,
        on_description,
        off_description: str,
        **kwargs,
    ):
        self.active = kwargs.get('active', False)
        self.on_description = on_description
        self.off_description = off_description
        self.object_type = 'activateable'
        super().__init__(
            id=id,
            name=name,
            description=self.on_description
            if self.active else self.off_description,
            **kwargs,
        )

    def turn_on(self, **kwargs) -> Tuple[str, str]:
        """Turn On action handler for Activateable objects..
        Returns:
            An Action result.
        """
        if self.active is True:
            return ActionResult(action_text=f'The {self.name} is already on.')
        self.active = True
        self.description = self.on_description
        return ActionResult(adventure_text=self.on_description,
                            action_text=f'You turn on the {self.name}.')

    def turn_off(self, **kwargs) -> Tuple[str, str]:
        """Turn Off action handler for Activatable objects.
        Returns:
            An Action result.
        """
        if self.active is False:
            return ActionResult(action_text=f'The {self.name} is already off.')
        self.active = False
        self.description = self.off_description
        return ActionResult(adventure_text=self.off_description,
                            action_text=f'You turn off the {self.name}.')

    def look(self, **kwargs) -> Tuple[str, str]:
        """Look action handler for Activateable objects.
        Returns:
            An Action result.
        """
        if self.active:
            return ActionResult(
                adventure_text=self.on_description,
                action_text=f'You take a closer look at the {self.name}.')
        else:
            return ActionResult(
                adventure_text=self.off_description,
                action_text=f'You take a closer look at the {self.name}.')
