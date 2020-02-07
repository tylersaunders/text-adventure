import './styles.scss';
import io from 'socket.io-client';

const socket = io();

const terminal = document.getElementById('terminal');
terminal.addEventListener('keyup', (e) => {
  if (e.keyCode === 13) {
    socket.emit('action', terminal.value);
    terminal.value = null;
  }
});

const display = document.getElementById('display-wrapper');

socket.on('connect', () => {
  console.log('connected!');
});

socket.on('adventure-text', (message) => {
  const node = document.createElement('p');
  node.textContent = message;
  display.appendChild(node);
});
