from enum import Enum


class Sockets(Enum):
    ACTION_TEXT = 'action-text'
    ADVENTURE_TITLE = 'adventure-title'
    ADVENTURE_TEXT = 'adventure-text'
    CONNECT = 'connect'
    INVENTORY = 'inventory'
    PLAYER_ACTIONS = 'player-action'
    START_GAME = 'start-game'
    LOAD_GAME = 'load-game'
    GAME_ID = 'game-id'


class ObjectTypes(Enum):
    ACTIVATEABLE = 'activateable'
    ADVENTURE_OBJECT = 'adventure_object'
