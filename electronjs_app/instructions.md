# Scientific and Geometric Calculator - Electron.js Application

## Overview
This is a modern desktop calculator application built with Electron.js that provides both scientific and geometric calculation capabilities. The application features a clean, user-friendly interface with support for basic arithmetic, advanced scientific functions, and geometric calculations.

## Project Structure
```
electronjs_app/
├── main.js         # Main Electron process
├── index.html      # Calculator UI
├── styles.css      # Application styling
├── renderer.js     # Calculator logic
├── terminal.html   # Terminal UI layout
├── terminal.js     # Terminal renderer and interaction logic
└── package.json    # Project configuration
```

## Features
### Scientific Functions
- Trigonometric calculations (sin, cos, tan)
- Logarithmic functions (log, ln)
- Square root
- Pi (π) constant
- Power operations

### Geometric Calculations
- Circle area
- Square area
- Triangle area
- Rectangle area

### Basic Operations
- Addition
- Subtraction
- Multiplication
- Division
- Clear function
- Decimal support

### Terminal Integration
- Integrated terminal window
- Supports bash (Linux/macOS) and PowerShell (Windows)
- Real-time command execution
- Error and exit status handling
- Scrollback buffer support

### Code Execution Subprocess

#### Features
- Execute code directly from the application
- Supports multiple languages:
  - Python
  - JavaScript
  - Shell commands
- Secure subprocess management
- Sandboxed execution environment
- Error handling and output capturing

#### Execution Methods
1. **Menu-based Execution**
   - Navigate to `File > Execute Code`
   - Choose language:
     - Run Python Script
     - Run JavaScript
     - Run Shell Command
   - Enter code in popup dialog
   - View execution results

2. **Programmatic Execution**
   ```javascript
   // In renderer process
   const result = await ipcRenderer.invoke('execute-code', {
     language: 'python',
     code: 'print("Hello, World!")'
   });
   ```

#### Security Considerations
- Temporary file creation for Python scripts
- Timeout mechanisms
- Sandboxed JavaScript execution
- Limited buffer size for shell commands
- Restricted execution time

#### Supported Languages
##### Python
- Uses `python3` interpreter
- Temporary script file generation
- Captures stdout and stderr
- Automatic file cleanup

##### JavaScript
- Uses `vm2` for safe execution
- Sandboxed environment
- 5-second execution timeout
- Prevents access to Node.js internals

##### Shell
- Executes system commands
- 10-second timeout
- 1MB output buffer
- Captures command output and errors

#### Limitations
- No persistent state between executions
- Limited to local machine capabilities
- Security risks with untrusted code
- Performance overhead for script execution

#### Best Practices
- Avoid executing untrusted code
- Keep scripts short and focused
- Handle potential errors gracefully
- Use appropriate language for the task

#### Future Improvements
- Add more language support
- Implement more robust sandboxing
- Create custom execution environments
- Add syntax highlighting for code input
- Implement code history and saved scripts

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install electron --save-dev
   ```

2. **Update package.json**
   Replace or update your package.json with:
   ```json
   {
     "name": "electronjs_app",
     "version": "1.0.0",
     "description": "Scientific and Geometric Calculator",
     "main": "main.js",
     "scripts": {
       "start": "electron ."
     },
     "keywords": [],
     "author": "",
     "license": "ISC",
     "devDependencies": {
       "electron": "latest"
     }
   }
   ```

3. **Run the Application**
   ```bash
   npm start
   ```

## Usage Guide

### Scientific Calculations
- Click any number to input it
- Use scientific function buttons (sin, cos, tan, log, ln, √, π) to perform calculations
- Results are displayed immediately

### Geometric Calculations
- Input the primary measurement (radius for circle, side for square, etc.)
- Click the desired shape button
- For rectangles, you'll be prompted to enter the height
- Area result will be displayed

### Basic Operations
- Enter the first number
- Click an operation (+, -, ×, /)
- Enter the second number
- Press = to see the result
- Use C to clear the display

### Terminal Interaction
- Open a new terminal via menu: `Terminal > New Terminal`
- Keyboard shortcut:
  - Windows/Linux: `Ctrl+T`
  - macOS: `Cmd+T`

## Development Notes
- The application uses vanilla JavaScript for calculations
- All scientific calculations are performed using JavaScript's Math object
- Geometric calculations include formulas for basic shapes
- The UI is built with HTML/CSS and features a responsive design
- Error handling is implemented for invalid inputs
- Terminal integration uses Electron's `child_process` for terminal spawning and `xterm.js` for terminal rendering and interaction

## Troubleshooting
- If the application doesn't start, ensure all dependencies are properly installed
- Check that all files (main.js, index.html, styles.css, renderer.js, terminal.html, terminal.js) are in the same directory
- Verify that the package.json has the correct configuration
- Make sure you have Node.js and npm installed on your system
- Ensure Node.js and Electron versions are compatible for terminal integration
- Check system shell configuration for terminal integration

## Network Troubleshooting

### Resolving NPM Installation Issues
If you encounter the error `getaddrinfo EAI_AGAIN github.com` or similar DNS-related issues, follow these steps in order:

1. **Clear NPM Cache**
```bash
npm cache clean --force
```

2. **Update DNS Configuration**
```bash
# Add Google DNS servers
echo -e "nameserver 8.8.8.8\nnameserver 8.8.4.4" | sudo tee /etc/resolv.conf
```

3. **Configure NPM Registry**
```bash
# Set primary registry
npm set registry https://registry.npmjs.org/

# If still failing, try alternative registry
npm install --save-dev electron --registry=https://registry.npmmirror.com
```

4. **Verify Connectivity**
```bash
# Test connection to GitHub
ping github.com
```

### Additional Network Solutions
- Check your internet connection
- Temporarily disable firewall
- Try using a VPN service
- If on corporate network, contact IT support
- Consider using offline installation methods

## Current Project Status

### Completed 
- Basic project structure created
  - main.js (Electron main process)
  - index.html (Calculator UI)
  - styles.css (Styling)
  - renderer.js (Calculator logic)
  - terminal.html (Terminal UI layout)
  - terminal.js (Terminal renderer and interaction logic)
- Package.json initialization

### Pending 
- Electron installation (blocked by DNS issues)
- Application first run
- Feature testing

### Next Steps
1. Complete dependency installation
2. Verify all files are properly loaded
3. Test calculator functionality
4. Document any additional issues

## Future Enhancements
- Add more geometric shapes and calculations
- Implement memory functions
- Add unit conversions
- Include angle mode switching (degrees/radians)
- Add keyboard support
- Implement history feature
- Add more advanced terminal features
- Implement shell customization options
- Enhance cross-platform compatibility