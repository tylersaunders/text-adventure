import * as socketIo from 'socket.io-client';

/**
 * An adventure terminal implementation that displays story text, action text
 * and accepts user input.
 */
export class AdventureTerminal {
  readonly INPUT_PLACEHOLDER = 'what next?';
  readonly INPUT_KEYS = [13];

  readonly host: HTMLElement;
  readonly adventureDisplay: HTMLDivElement;
  readonly actionDisplay: HTMLDivElement;
  readonly input: HTMLInputElement;

  constructor(private readonly _socket: SocketIOClient.Socket) {
    this.host = document.createElement('div');
    document.body.append(this.host);
    this.host.classList.add('console');

    // Build Display.
    this.adventureDisplay = document.createElement('div');
    this.adventureDisplay.classList.add('adventure-text');
    this.host.appendChild(this.adventureDisplay);

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

    this.host.appendChild(terminalWrapper);

    this.setupSockets();
  }

  setupSockets(): void {
    this._socket.on('adventure-text', (message: string) => {
      this.adventureDisplay.textContent = message;
    });

    this._socket.on('action-text', (message: string) => {
      this.actionDisplay.textContent = message;
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
