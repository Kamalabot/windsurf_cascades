# WebAssembly Calculator Application

## Project Overview
A feature-rich calculator application built using Rust (compiled to WebAssembly) and JavaScript/HTML for the user interface. This calculator provides both basic arithmetic operations and advanced mathematical functions in a modern web-based interface.

## Technical Stack
- **Backend Language**: Rust
- **Compilation Target**: WebAssembly (wasm)
- **Frontend**: HTML5, CSS3, JavaScript
- **Build Tools**: wasm-pack, webpack
- **Project Structure**: Module-based Design

## Features

### Basic Operations
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Clear entry (CE)
- Clear all (C)
- Backspace function

### Trigonometric Functions
- Sine (sin)
- Cosine (cos)
- Tangent (tan)
- Inverse sine (arcsin)
- Inverse cosine (arccos)
- Inverse tangent (arctan)
- Option to switch between degrees and radians
- Hyperbolic functions (sinh, cosh, tanh)

### Advanced Operations
- Square root (√)
- Power/Exponent (x²)
- Percentage calculations (%)
- Negative/Positive toggle (+/-)
- Decimal point operations

### User Interface Features
- Modern and responsive web design
- Button click animations
- Error handling and display
- History of calculations
- Keyboard support for number input
- Copy/Paste functionality
- Mobile-responsive layout

### Memory Functions
- Memory Store (MS)
- Memory Recall (MR)
- Memory Clear (MC)
- Memory Add (M+)
- Memory Subtract (M-)

### Additional Features
- Scientific notation for large numbers
- Error handling for division by zero
- Expression validation
- Responsive design for all screen sizes
- Offline functionality using Service Workers
- High-performance calculations using WASM

## Setup and Running Instructions

### Prerequisites
- Rust and Cargo (latest stable version)
- Node.js and npm (v14 or later)
- wasm-pack (`cargo install wasm-pack`)
- A modern web browser with WebAssembly support

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wasm-calculator.git
   cd wasm-calculator
   ```

2. Build the WebAssembly module:
   ```bash
   cd wasm-calculator
   wasm-pack build
   ```

3. Install web dependencies:
   ```bash
   cd www
   npm install
   ```

### Running the Application
1. Start the development server:
   ```bash
   cd www
   npm run start
   ```

2. Access the calculator:
   - Open your web browser
   - Navigate to `http://localhost:8080`
   - The calculator interface should load automatically

### Development
- The Rust source code is in the `src` directory
- Web interface files are in the `www` directory
- After making changes to Rust code, rebuild using `wasm-pack build`
- Changes to web files (HTML, CSS, JS) will auto-reload

### Building for Production
1. Build the WebAssembly module in release mode:
   ```bash
   wasm-pack build --release
   ```

2. Build the web interface:
   ```bash
   cd www
   npm run build
   ```

3. The production files will be in `www/dist` directory

## Future Enhancements
- Scientific calculator mode
- Unit conversion capabilities
- Custom themes with CSS variables
- Calculation history export to CSV/JSON
- Programmer's calculator mode
- Geometric calculator mode

### Geometric Calculator
- Area of a circle (A)
- Area of a rectangle (A)
- Area of a triangle (A)
- Perimeter of a circle (P)
- Perimeter of a rectangle (P)
- Perimeter of a triangle (P)
- Volume of a sphere (V)
- Volume of a cylinder (V)
- Volume of a cone (V)
- Volume of a cube (V) 

#### Geometric Calculator Features
- Each shape will have a dynamic SVG-based UI
- Interactive shape manipulation
- Real-time calculation updates
- Comprehensive test suite for each shape

## Project Structure
```
calculator/
├── src/
│   ├── lib.rs          # Rust library code
│   ├── calculator.rs    # Core calculator logic
│   └── utils.rs        # Utility functions
├── www/
│   ├── index.html      # Main HTML file
│   ├── style.css       # Styles
│   ├── index.js        # JavaScript entry point
│   └── components/     # UI components
├── tests/              # Test files
├── Cargo.toml          # Rust dependencies
├── package.json        # Node.js dependencies
├── webpack.config.js   # Webpack configuration
└── README.md          # Project documentation

## Development Guidelines
- Follow Rust coding conventions
- Implement comprehensive error handling
- Add documentation for all public functions
- Include unit tests for Rust code
- Include integration tests for JS-WASM interaction
- Maintain clean and modular code structure
- Optimize WASM binary size
- Follow web accessibility guidelines (WCAG)
