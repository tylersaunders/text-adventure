from server.engine.location import Location
from server.engine.scenario import Scenario
from server.engine.object import Activateable

first_room = Location(
    'You are in a dimly lit cabin, high in the rocky mountains. \n'
    ' On a small side table near the corner is a lamp. \n'
    'To the north is a grimey cave.')

second_room = Location('A grimy cave in the middle of nowhere. \n'
                       'Behind you is a cabin in the woods.')

first_room.exits = {'north': second_room}
second_room.exits = {'south': first_room}

lamp = Activateable('lamp', 'A small bronze table lamp.',
                    'The lamp throws a soft light throughout the room.',
                    'The bulb is cold and dusty.')
first_room.objects.append(lamp)

scenario = Scenario('A dark, cold winter', first_room)
