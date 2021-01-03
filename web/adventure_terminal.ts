import * as socketIo from 'socket.io-client';
import {Actions, Directions} from './enums';

/**
 * An adventure terminal implementation that displays story text, action text
 * and accepts user input.
 */
export class AdventureTerminal {
  readonly INPUT_PLACEHOLDER = 'what next?';
  readonly INPUT_KEYS = [13];
  readonly ACTION_KEYS = Object.values(Actions);
  readonly DIRECTION_KEYS = Object.values(Directions);

  readonly host: HTMLElement;
  readonly console: HTMLElement;
  readonly title: HTMLElement;
  readonly adventureDisplay: HTMLDivElement;
  readonly actionDisplay: HTMLDivElement;
  readonly input: HTMLInputElement;
  readonly actionHints:HTMLDivElement;

  constructor(private readonly _socket: SocketIOClient.Socket) {
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
    this.input.addEventListener('keyup', (e) => {
      if (this.INPUT_KEYS.includes(e.keyCode)) {
        this.sendAction(this.input.value);
        this.input.value = '';
      }
    });
    terminalWrapper.appendChild(this.input);

    this.console.appendChild(terminalWrapper);

    this.actionHints = document.createElement('div');
    this.actionHints.classList.add('action-hints');
    const actionDiv = document.createElement('div');
    const actionText = document.createElement('p');
    actionText.textContent = 'actions';
    const actionKeys = document.createElement('ul');
    for(const key of this.ACTION_KEYS){
      const li = document.createElement('li');
      li.textContent = key;
      actionKeys.appendChild(li);
    }
    actionDiv.append(actionText,actionKeys);

    const directionDiv = document.createElement('div');
    const directionText = document.createElement('p');
    directionText.textContent = 'directions';
    const directionKeys = document.createElement('ul');
    for(const key of this.DIRECTION_KEYS){
      const li = document.createElement('li');
      li.textContent = key;
      directionKeys.appendChild(li);
    }
    directionDiv.append(directionText,directionKeys);

    this.actionHints.append(actionDiv, directionDiv);

    this.host.append(this.console,this.actionHints);
    document.body.append(this.host);

    this.setupSockets();
  }

  setupSockets(): void {
    this._socket.on('adventure-title', (message:string)=>{
      this.title.textContent = message;
    })

    this._socket.on('adventure-text', (message: string) => {
      this.adventureDisplay.textContent = message;
    });

    this._socket.on('action-text', (message: string) => {
      this.actionDisplay.textContent = message;
    });

    this._socket.on('game-id', (gameId:string)=>{
      // When a new game-id is recieved from the server, stash it in a browser cookie.
      const expires = new Date(9999,1,1);
      document.cookie = `gameId=${gameId};expires=${expires.toUTCString()}`
    })

    this._socket.on('connect', (message:string)=>{
      // Check and see if we have a current game-id already stored in browser cookies.
      const cookies = document.cookie.split(';');
      const gameId = cookies.find(row=>row.startsWith('gameId'))?.split('=')[1];
      if(gameId){
        this._socket.emit('load-game', gameId);
      } else {
        this._socket.emit('start-game');
      }
    });
  }

  /**
   * Send a user action through the current socket.
   * @param action
   */
  sendAction(action: string): void {
    this._socket.emit('player-action', action);
  }
}
