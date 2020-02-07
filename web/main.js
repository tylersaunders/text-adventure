import './styles.scss';
import io from 'socket.io-client';

const socket = io();

socket.on('connect', () => {
  console.log('connected!');
});

const terminal = document.getElementById('terminal');
terminal.focus();
terminal.addEventListener('keyup', (e) => {
  if (e.keyCode === 13) {
    socket.emit('action', terminal.value);
    terminal.value = null;
  }
});

const adventureText = document.getElementById('adventure-text');

socket.on('adventure-text', (message) => {
  adventureText.textContent = message;
});

const actionText = document.getElementById('action-text');

socket.on('action-text', (message) => {
  actionText.textContent = message;
});
