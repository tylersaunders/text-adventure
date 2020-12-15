import 'jasmine';
import {AdventureTerminal} from '../web/adventure_terminal';

describe('text-adventure', () => {
  it('should create a new adventure terminal', () => {
    const adventureText = document.querySelector('.adventure-text');
    const terminalWrapper = document.querySelector('.terminal-wrapper');
    const actionDisplay = document.querySelector('.action-text');
    const input = document.querySelector('.terminal');

    expect(adventureText).toBeTruthy();
    expect(terminalWrapper).toBeTruthy();
    expect(actionDisplay).toBeTruthy();
    expect(input).toBeTruthy();
  });
});
