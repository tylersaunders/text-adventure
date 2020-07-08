import 'jasmine';
import {AdventureTerminal} from '../web/adventure_terminal';

describe('text-adventure', () => {
  it('should create a new adventure terminal', () => {
    const adventureText = document.getElementById('adventure-text');
    const terminalWrapper = document.getElementById('terminal-wrapper');
    const actionDisplay = document.getElementById('action-text');
    const input = document.getElementById('terminal');

    expect(adventureText).toBeTruthy();
    expect(terminalWrapper).toBeTruthy();
    expect(actionDisplay).toBeTruthy();
    expect(input).toBeTruthy();
  });
});
