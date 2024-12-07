let display = document.getElementById('display');
let currentInput = '';
let currentOperation = null;
let previousInput = '';
let shouldStartNewNumber = false;  // New flag to indicate when to start a new number

function appendNumber(num) {
    if (shouldStartNewNumber) {
        currentInput = num;
        shouldStartNewNumber = false;
    } else {
        currentInput += num;
    }
    updateDisplay();
}

function appendOperator(operator) {
    if (currentInput !== '') {
        previousInput = currentInput;
        currentInput = previousInput;
        currentOperation = operator;
        shouldStartNewNumber = true;  // Set flag to true when operator is pressed
        updateDisplay();
    }
}

function clearDisplay() {
    currentInput = '';
    previousInput = '';
    currentOperation = null;
    shouldStartNewNumber = false;
    updateDisplay();
}

function updateDisplay() {
    display.value = currentInput || '0';
}

function calculate(operation) {
    if (operation === 'equals' && previousInput !== '' && currentInput !== '') {
        let result;
        const prev = parseFloat(previousInput);
        const current = parseFloat(currentInput);

        switch (currentOperation) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                result = prev / current;
                break;
        }

        currentInput = result.toString();
        previousInput = '';
        currentOperation = null;
        shouldStartNewNumber = false;
        updateDisplay();
    } else {
        // Scientific calculations
        let result;
        const current = parseFloat(currentInput);

        switch (operation) {
            case 'sin':
                result = Math.sin(current * Math.PI / 180);
                break;
            case 'cos':
                result = Math.cos(current * Math.PI / 180);
                break;
            case 'tan':
                result = Math.tan(current * Math.PI / 180);
                break;
            case 'log':
                result = Math.log10(current);
                break;
            case 'ln':
                result = Math.log(current);
                break;
            case 'sqrt':
                result = Math.sqrt(current);
                break;
            case 'pi':
                result = Math.PI;
                break;
        }

        if (result !== undefined) {
            currentInput = result.toString();
            updateDisplay();
        }
    }
}

function geometric(shape) {
    let result;
    const current = parseFloat(currentInput);

    switch (shape) {
        case 'circle':
            // Area of circle
            result = Math.PI * current * current;
            break;
        case 'square':
            // Area of square
            result = current * current;
            break;
        case 'triangle':
            // Area of equilateral triangle
            result = (Math.sqrt(3) / 4) * current * current;
            break;
        case 'rectangle':
            // Prompt for height (current is width)
            const height = prompt('Enter height:');
            if (height) {
                result = current * parseFloat(height);
            }
            break;
    }

    if (result !== undefined) {
        currentInput = result.toString();
        updateDisplay();
    }
}

// Initialize display
updateDisplay();
