"""Location classes for text-adventure."""


class Location():
    """A location in a scenario. (Such as a room or place)."""
    description: str

    def __init__(self, description: str) -> None:
        self.description = description
