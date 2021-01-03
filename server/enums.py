from enum import Enum


class Sockets(Enum):
    CONNECT = 'connect'
    ADVENTURE_TITLE = 'adventure-title'
    ADVENTURE_TEXT = 'adventure-text'
    ACTION_TEXT = 'action-text'
    PLAYER_ACTIONS = 'player-action'
    START_GAME = 'start-game'
    LOAD_GAME = 'load-game'
    GAME_ID = 'game-id'
