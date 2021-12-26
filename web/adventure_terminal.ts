import {Socket} from 'socket.io-client';

import {Actions, Directions} from './enums';

/**
 * An adventure terminal implementation that displays story text, action text
 * and accepts user input.
 */
export class AdventureTerminal {
  readonly INPUT_PLACEHOLDER = 'what next?';
  readonly INPUT_KEYS = ['Enter'];
  readonly ACTION_KEYS = Object.values(Actions);
  readonly DIRECTION_KEYS = Object.values(Directions);

  readonly host: HTMLElement;
  readonly console: HTMLElement;
  readonly title: HTMLElement;
  readonly adventureDisplay: HTMLDivElement;
  readonly actionDisplay: HTMLDivElement;
  readonly input: HTMLInputElement;
  readonly infoPanel: HTMLDivElement;
  readonly inventoryList: HTMLElement;

  constructor(private readonly _socket: Socket) {
    this.host = document.createElement('div');
    this.host.classList.add('adventure-terminal');
    this.title = document.createElement('p');
    this.title.classList.add('title');
    this.host.append(this.title);

    this.console = document.createElement('div');
    this.console.classList.add('console');

    // Build Display.
    this.adventureDisplay = document.createElement('div');
    this.adventureDisplay.classList.add('adventure-text');
    this.console.appendChild(this.adventureDisplay);

    // Build Terminal Input.
    const terminalWrapper = document.createElement('div');
    terminalWrapper.classList.add('terminal-wrapper');

    this.actionDisplay = document.createElement('div');
    this.actionDisplay.classList.add('action-text');
    terminalWrapper.appendChild(this.actionDisplay);

    this.input = document.createElement('input');
    this.input.classList.add('terminal');
    this.input.placeholder = this.INPUT_PLACEHOLDER;
    this.input.addEventListener('keyup', (event: KeyboardEvent) => {
      if (this.INPUT_KEYS.includes(event.code)) {
        this.sendAction(this.input.value);
        this.input.value = '';
      }
    });
    terminalWrapper.appendChild(this.input);

    this.console.appendChild(terminalWrapper);

    this.infoPanel = document.createElement('div');
    this.infoPanel.classList.add('info-panel');
    const actionDiv = document.createElement('div');
    const actionText = document.createElement('p');
    actionText.textContent = 'actions';
    const actionKeys = document.createElement('ul');
    for (const key of this.ACTION_KEYS) {
      const li = document.createElement('li');
      li.textContent = key;
      actionKeys.appendChild(li);
    }
    actionDiv.append(actionText, actionKeys);

    const directionDiv = document.createElement('div');
    const directionText = document.createElement('p');
    directionText.textContent = 'directions';
    const directionKeys = document.createElement('ul');
    for (const key of this.DIRECTION_KEYS) {
      const li = document.createElement('li');
      li.textContent = key;
      directionKeys.appendChild(li);
    }
    directionDiv.append(directionText, directionKeys);

    const inventoryWrapper = document.createElement('div');
    inventoryWrapper.classList.add('inventory-wrapper');
    const inventoryText = document.createElement('p');
    inventoryText.innerText = 'inventory';
    inventoryWrapper.appendChild(inventoryText);
    this.inventoryList = document.createElement('ul');
    inventoryWrapper.appendChild(this.inventoryList);

    this.infoPanel.append(actionDiv, directionDiv, inventoryWrapper);

    this.host.append(this.console, this.infoPanel);
    document.body.append(this.host);

    this.setupSockets();
  }

  /**
   * Set up socket listeners for backend websocket channels.
   */
  private setupSockets(): void {
    this._socket.on('adventure-title', this.onAdventureTitle.bind(this));
    this._socket.on('adventure-text', this.onAdventureText.bind(this));
    this._socket.on('action-text', this.onActionText.bind(this));
    this._socket.on('game-id', this.onGameId.bind(this));
    this._socket.on('connect', this.onConnect.bind(this));
    this._socket.on('inventory', this.onInventoryMessage.bind(this));
    this._socket.on('ending', this.onEnding.bind(this));
  }

  private onConnect(): void {
    // Check and see if we have a current game-id already stored in
    // browser cookies.
    const cookies = document.cookie.split(';');
    const gameId = cookies.find(row => row.startsWith('gameId'))?.split('=')[1];
    if (gameId) {
      this._socket.emit('load-game', gameId);
    } else {
      this._socket.emit('start-game');
    }
  }

  private onGameId(gameId: string): void {
    // When a new game-id is recieved from the server, stash it in a
    // browser cookie.
    const expires = new Date(9999, 1, 1);
    document.cookie = `gameId=${gameId};expires=${expires.toUTCString()}`
  }

  private onAdventureTitle(title: string): void {
    this.title.textContent = title;
    document.title = title;
  }

  private onActionText(message: string): void {
    this.actionDisplay.textContent = message;
  }

  private onAdventureText(message: string): void {
    this.adventureDisplay.textContent = message;
  }

  private onEnding(message: string): void {
    // Remove all UI elements.
    while (this.host.firstChild) {
      this.host.removeChild(this.host.firstChild);
    }

    const endingMessage = document.createElement('div');
    endingMessage.innerText = message;
    endingMessage.classList.add('ending-message');
    const theEnd = document.createElement('div');
    theEnd.textContent = 'The End';
    theEnd.classList.add('the-end');

    this.host.appendChild(endingMessage);
    this.host.appendChild(theEnd);

    // Remove the game Id as this one is over.
    document.cookie = `gameId=${undefined};expires=${new Date()}`;
  }

  private onInventoryMessage(message: string): void {
    // Assume message is a comma seperated list of item names
    // i.e. key,coffee mug,amulet of truth
    const inventory = message.split(',');
    while (this.inventoryList.lastChild) {
      this.inventoryList.removeChild(this.inventoryList.lastChild);
    }
    for (const item of inventory) {
      const li = document.createElement('li');
      li.textContent = item;
      this.inventoryList.appendChild(li);
    }
  }

  /**
   * Send a user action through the current websocket.
   * @param action
   */
  private sendAction(action: string): void {
    this._socket.emit('player-action', action);
  }
}
