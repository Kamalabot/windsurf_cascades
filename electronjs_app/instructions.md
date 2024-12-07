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

## Development Notes
- The application uses vanilla JavaScript for calculations
- All scientific calculations are performed using JavaScript's Math object
- Geometric calculations include formulas for basic shapes
- The UI is built with HTML/CSS and features a responsive design
- Error handling is implemented for invalid inputs

## Troubleshooting
- If the application doesn't start, ensure all dependencies are properly installed
- Check that all files (main.js, index.html, styles.css, renderer.js) are in the same directory
- Verify that the package.json has the correct configuration
- Make sure you have Node.js and npm installed on your system

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