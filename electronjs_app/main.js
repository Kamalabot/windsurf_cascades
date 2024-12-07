const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron');
const path = require('path');
const os = require('os');
const { spawn, exec } = require('child_process');
const fs = require('fs');

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
                    label: 'Execute Code',
                    submenu: [
                        {
                            label: 'Run Python Script',
                            click: () => executeCodePrompt('python')
                        },
                        {
                            label: 'Run JavaScript',
                            click: () => executeCodePrompt('javascript')
                        },
                        {
                            label: 'Run Shell Command',
                            click: () => executeCodePrompt('shell')
                        }
                    ]
                },
                { type: 'separator' },
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

    // Setup IPC listeners for code execution
    setupCodeExecutionListeners(win);
}

function setupCodeExecutionListeners(mainWindow) {
    // Execute code from renderer process
    ipcMain.handle('execute-code', async (event, { language, code }) => {
        return await executeCode(language, code);
    });
}

async function executeCode(language, code) {
    return new Promise((resolve, reject) => {
        // Temporary file for code execution
        const tempDir = os.tmpdir();
        const timestamp = Date.now();
        
        try {
            switch(language) {
                case 'python': {
                    const tempPyFile = path.join(tempDir, `temp_script_${timestamp}.py`);
                    fs.writeFileSync(tempPyFile, code);
                    
                    const pythonProcess = spawn('python3', [tempPyFile]);
                    
                    let output = '';
                    let errorOutput = '';
                    
                    pythonProcess.stdout.on('data', (data) => {
                        output += data.toString();
                    });
                    
                    pythonProcess.stderr.on('data', (data) => {
                        errorOutput += data.toString();
                    });
                    
                    pythonProcess.on('close', (code) => {
                        // Clean up temp file
                        fs.unlinkSync(tempPyFile);
                        
                        if (code === 0) {
                            resolve({ 
                                success: true, 
                                output: output.trim(), 
                                error: null 
                            });
                        } else {
                            resolve({ 
                                success: false, 
                                output: null, 
                                error: errorOutput.trim() 
                            });
                        }
                    });
                    break;
                }
                
                case 'javascript': {
                    try {
                        // Use vm module for safe JavaScript execution
                        const { VM } = require('vm2');
                        const vm = new VM({
                            timeout: 5000,
                            sandbox: {}
                        });
                        
                        const result = vm.run(code);
                        resolve({
                            success: true,
                            output: result ? result.toString() : 'Execution completed',
                            error: null
                        });
                    } catch (error) {
                        resolve({
                            success: false,
                            output: null,
                            error: error.toString()
                        });
                    }
                    break;
                }
                
                case 'shell': {
                    exec(code, { 
                        maxBuffer: 1024 * 1024,  // 1MB buffer
                        timeout: 10000  // 10 seconds timeout
                    }, (error, stdout, stderr) => {
                        if (error) {
                            resolve({
                                success: false,
                                output: null,
                                error: error.message
                            });
                            return;
                        }
                        
                        resolve({
                            success: true,
                            output: stdout.trim(),
                            error: stderr ? stderr.trim() : null
                        });
                    });
                    break;
                }
                
                default:
                    reject(new Error('Unsupported language'));
            }
        } catch (error) {
            resolve({
                success: false,
                output: null,
                error: error.toString()
            });
        }
    });
}

function executeCodePrompt(language) {
    const mainWindow = BrowserWindow.getFocusedWindow();
    
    dialog.showMessageBox(mainWindow, {
        type: 'question',
        buttons: ['OK', 'Cancel'],
        defaultId: 0,
        title: `Execute ${language.toUpperCase()} Code`,
        message: `Enter your ${language} code:`,
        inputType: 'textarea'
    }).then(result => {
        if (result.response === 0) {  // OK button
            const code = result.inputValue;
            
            executeCode(language, code)
                .then(result => {
                    dialog.showMessageBox(mainWindow, {
                        type: result.success ? 'info' : 'error',
                        title: result.success ? 'Execution Successful' : 'Execution Failed',
                        message: result.success ? 
                            `Output:\n${result.output}` : 
                            `Error:\n${result.error}`
                    });
                })
                .catch(error => {
                    dialog.showMessageBox(mainWindow, {
                        type: 'error',
                        title: 'Execution Error',
                        message: error.toString()
                    });
                });
        }
    });
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
