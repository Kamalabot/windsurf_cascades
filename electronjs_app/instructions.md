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

## Future Enhancements
- Add more geometric shapes and calculations
- Implement memory functions
- Add unit conversions
- Include angle mode switching (degrees/radians)
- Add keyboard support
- Implement history feature
