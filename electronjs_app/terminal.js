const { Terminal } = require('@xterm/xterm');
const { ipcRenderer } = require('electron');

// Initialize terminal with better defaults
const term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    theme: {
        background: '#1e1e1e',
        foreground: '#ffffff',
        cursor: '#ffffff',
        selection: '#4040408c'
    },
    allowTransparency: true,
    scrollback: 1000,
    cols: 80,
    rows: 24
});

// Create terminal
const terminalElement = document.getElementById('terminal');
term.open(terminalElement);

// Set initial focus
term.focus();

// Handle terminal input
term.onData(data => {
    ipcRenderer.send('terminal-input', data);
});

// Handle terminal output
ipcRenderer.on('terminal-output', (event, data) => {
    term.write(data);
});

// Handle terminal exit
ipcRenderer.on('terminal-exit', (event, { exitCode, signal }) => {
    term.write(`\r\nProcess exited with code ${exitCode}${signal ? ` (signal: ${signal})` : ''}\r\n`);
});

// Handle terminal errors
ipcRenderer.on('terminal-error', (event, errorMessage) => {
    term.write(`\r\n\x1b[1;31mError: ${errorMessage}\x1b[0m\r\n`);
});

// Handle terminal resize
const fitTerminal = () => {
    const dims = {
        cols: Math.floor((terminalElement.clientWidth) / 9),
        rows: Math.floor((terminalElement.clientHeight - 10) / 17)
    };
    term.resize(dims.cols, dims.rows);
    ipcRenderer.send('terminal-resize', dims);
};

// Initial fit
setTimeout(fitTerminal, 100);

// Handle window resize
window.addEventListener('resize', () => {
    fitTerminal();
});

// Write welcome message
term.write('\x1b[1;34m=== Calculator Terminal ===\x1b[0m\r\n\r\n');
