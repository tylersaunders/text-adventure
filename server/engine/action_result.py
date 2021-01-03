from dataclasses import dataclass


@dataclass
class ActionResult:
    """A helper/typing class for the responses for actions.

    This ResultType will provide the required data for the adventure engine
    to correctly return a response to the player.
    """
    adventure_text: str = None
    action_text: str = None
    push_inventory_update: bool = False
