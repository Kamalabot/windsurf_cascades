import { init_wasm, Calculator } from 'wasm-calculator';

let calculator = null;
let display = null;
let currentInput = '0';
let newNumber = true;
let initialized = false;
let lastOperation = null;

async function initCalculator() {
    if (initialized) return;

    try {
        await init_wasm();
        calculator = new Calculator();
        display = document.getElementById('display');
        if (!display) {
            throw new Error('Display element not found');
        }
        initialized = true;
        updateDisplay();
        console.log('Calculator initialized successfully');
    } catch (error) {
        console.error('Failed to initialize calculator:', error);
        display = document.getElementById('display');
        if (display) {
            display.textContent = 'Error: Failed to initialize';
        }
        throw error;
    }
}

function ensureInitialized() {
    if (!initialized || !calculator) {
        throw new Error('Calculator not initialized');
    }
}

window.appendNumber = async (number) => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        if (number === '.' && currentInput.includes('.')) {
            return;
        }

        if (newNumber) {
            currentInput = number === '.' ? '0.' : number;
            newNumber = false;
        } else {
            currentInput = currentInput === '0' && number !== '.' 
                ? number 
                : currentInput + number;
        }
        
        updateDisplay();
    } catch (error) {
        handleError(error);
    }
};

window.setOperation = async (op) => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        const value = parseFloat(currentInput);
        let result;
        
        switch(op) {
            case '+':
                result = calculator.add(value);
                break;
            case '-':
                result = calculator.subtract(value);
                break;
            case '*':
                result = calculator.multiply(value);
                break;
            case '/':
                if (value === 0) {
                    throw new Error('Division by zero');
                }
                result = calculator.divide(value);
                break;
        }
        
        currentInput = result.toString();
        updateDisplay();
        lastOperation = op;
        newNumber = true;
    } catch (error) {
        handleError(error);
    }
};

window.calculate = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        const value = parseFloat(currentInput);
        const result = calculator.equals();
        currentInput = result.toString();
        updateDisplay();
        newNumber = true;
        lastOperation = null;
    } catch (error) {
        handleError(error);
    }
};

window.clearDisplay = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        calculator.clear();
        currentInput = '0';
        newNumber = true;
        lastOperation = null;
        updateDisplay();
    } catch (error) {
        handleError(error);
    }
};

window.toggleSign = () => {
    try {
        if (currentInput !== '0') {
            currentInput = (-parseFloat(currentInput)).toString();
            updateDisplay();
        }
    } catch (error) {
        handleError(error);
    }
};

window.calculatePercent = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        const value = parseFloat(currentInput);
        currentInput = (value / 100).toString();
        updateDisplay();
        newNumber = false;
    } catch (error) {
        handleError(error);
    }
};

// Memory functions
window.memoryStore = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        calculator.memory_store();
    } catch (error) {
        handleError(error);
    }
};

window.memoryRecall = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        currentInput = calculator.memory_recall().toString();
        updateDisplay();
        newNumber = true;
    } catch (error) {
        handleError(error);
    }
};

window.memoryAdd = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        calculator.memory_add();
    } catch (error) {
        handleError(error);
    }
};

window.memoryClear = async () => {
    try {
        if (!initialized) {
            await initCalculator();
        }
        
        ensureInitialized();
        calculator.memory_clear();
    } catch (error) {
        handleError(error);
    }
};

function updateDisplay() {
    if (display) {
        // Format the number to avoid floating point precision issues
        const num = parseFloat(currentInput);
        if (isNaN(num)) {
            display.textContent = 'Error';
        } else {
            display.textContent = num.toString();
        }
    }
}

function handleError(error) {
    console.error('Calculator error:', error);
    if (display) {
        display.textContent = 'Error';
    }
    currentInput = '0';
    newNumber = true;
    lastOperation = null;
}

// Initialize calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    initCalculator().catch(error => {
        console.error('Failed to initialize calculator on load:', error);
    });
});
