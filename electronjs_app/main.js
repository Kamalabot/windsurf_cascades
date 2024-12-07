const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');

// Initialize shell
const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';
let terminalProcess;

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');

    // Create menu template
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Exit',
                    accelerator: process.platform === 'darwin' ? 'Command+Q' : 'Alt+F4',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: 'Terminal',
            submenu: [
                {
                    label: 'New Terminal',
                    accelerator: process.platform === 'darwin' ? 'Command+T' : 'Ctrl+T',
                    click: () => {
                        createTerminalWindow();
                    }
                }
            ]
        }
    ];

    // Create menu
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function createTerminalWindow() {
    const terminalWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        title: 'Terminal'
    });

    terminalWindow.loadFile('terminal.html');

    try {
        // Create terminal process
        terminalProcess = spawn(shell, [], {
            env: process.env,
            cwd: os.homedir()
        });

        // Handle terminal data
        terminalProcess.stdout.on('data', (data) => {
            if (!terminalWindow.isDestroyed()) {
                terminalWindow.webContents.send('terminal-output', data.toString());
            }
        });

        terminalProcess.stderr.on('data', (data) => {
            if (!terminalWindow.isDestroyed()) {
                terminalWindow.webContents.send('terminal-output', data.toString());
            }
        });

        // Handle terminal exit
        terminalProcess.on('exit', (code, signal) => {
            if (!terminalWindow.isDestroyed()) {
                terminalWindow.webContents.send('terminal-exit', { code, signal });
            }
        });

        // Handle terminal error
        terminalProcess.on('error', (error) => {
            if (!terminalWindow.isDestroyed()) {
                terminalWindow.webContents.send('terminal-error', error.message);
            }
        });

        // Clean up when window is closed
        terminalWindow.on('closed', () => {
            if (terminalProcess) {
                terminalProcess.kill();
            }
        });

        // Handle IPC messages
        ipcMain.on('terminal-input', (event, data) => {
            if (terminalProcess && !terminalProcess.killed) {
                terminalProcess.stdin.write(data);
            }
        });

    } catch (error) {
        console.error('Failed to create terminal process:', error);
        if (!terminalWindow.isDestroyed()) {
            terminalWindow.webContents.send('terminal-error', error.message);
        }
    }
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
