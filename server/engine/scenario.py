from server.engine.location import Location


class Scenario():
    UNKNOWN_ACTION_RESPONSE: str = 'You aren\'t so sure about that.'
    locations = []
    player_location: Location = None
    greeting: str = ''
    """A text adventure scenario."""
    def __init__(self, greeting: str, starting_location: Location):
        self.greeting = greeting
        self.player_location = starting_location
        if starting_location not in self.locations:
            self.add_location(starting_location)

    def add_location(self, loc: Location) -> None:
        self.locations.append(loc)
        pass

    def move(self, direction: str):
        if direction in self.player_location.exits:
            self.player_location = self.player_location.exits[direction]
            return (self.player_location.look(), f'You travel {direction}.')
        else:
            return (None, 'You cannot go that way.')
