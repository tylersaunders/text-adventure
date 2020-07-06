import * as socketIo from 'socket.io-client';

const socket = socketIo.connect();

socket.on('connect', () => {
  console.log('connected!');
});

const terminal = document.getElementById('terminal') as HTMLInputElement;
terminal?.focus();
terminal?.addEventListener('keyup', (e) => {
  if (e.keyCode === 13) {
    socket.emit('action', terminal.value);
    terminal.value = '';
  }
});

const adventureText = document.getElementById('adventure-text') as HTMLDivElement;

socket.on('adventure-text', (message:string) => {
  adventureText.textContent = message;
});

const actionText = document.getElementById('action-text') as HTMLDivElement;

socket.on('action-text', (message:string) => {
  actionText.textContent = message;
});
