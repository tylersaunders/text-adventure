import * as socketIo from 'socket.io-client';
import {AdventureTerminal} from './adventure_terminal';

const socket = socketIo.connect('localhost:5000');
const terminal = new AdventureTerminal(socket);

terminal.input.focus();
