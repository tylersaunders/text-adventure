from server.engine.location import Location
from server.engine.scenario import Scenario

first_room = Location(
    'You are in a dimly lit cabin, high in the rocky mountains.')
second_room = Location('A grimy cave in the middle of nowhere.')
first_room.exits = {'north': second_room}
second_room.exits = {'south': first_room}
scenario = Scenario('A dark, cold winter', first_room)
