import * as socketIo from 'socket.io-client';

import {AdventureTerminal} from './adventure_terminal';

console.log('pre-connect');
const socket = socketIo.connect('localhost:5000');
socket.on('connect_error', console.log);
const terminal = new AdventureTerminal(socket);

terminal.input.focus();
