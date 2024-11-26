import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic

class CalculatorUI:
    def __init__(self, parent):
        self.parent = parent
        self.calc = CalculatorLogic()
        self.current_number = tk.StringVar(value="0")
        self.expression = []
        self.last_was_operator = False
        
        # If parent is root window, set title
        if isinstance(parent, tk.Tk):
            parent.title("Scientific Calculator")
            parent.configure(bg='#f0f0f0')
        
        self._create_display()
        self._create_buttons()
        self._setup_keyboard_bindings()

    def _create_display(self):
        display_frame = ttk.Frame(self.parent)
        display_frame.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
        
        self.display = ttk.Entry(
            display_frame,
            textvariable=self.current_number,
            justify="right",
            font=('Arial', 20),
            state='readonly'
        )
        self.display.grid(row=0, column=0, sticky="nsew")

    def _create_buttons(self):
        buttons_frame = ttk.Frame(self.parent)
        buttons_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        # Button layout
        button_layout = [
            ['MC', 'MR', 'MS', 'M+', 'M-'],
            ['deg', '(', ')', 'C', '⌫'],
            ['sin', 'cos', 'tan', '√', 'x²'],
            ['7', '8', '9', '÷', '%'],
            ['4', '5', '6', '×', '±'],
            ['1', '2', '3', '-', '1/x'],
            ['0', '.', '=', '+', 'π']
        ]

        for i, row in enumerate(button_layout):
            for j, text in enumerate(row):
                btn = ttk.Button(
                    buttons_frame,
                    text=text,
                    width=5,
                    command=lambda t=text: self._button_click(t)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)

    def _setup_keyboard_bindings(self):
        if isinstance(self.parent, tk.Tk):
            self.parent.bind('<Key>', self._handle_keypress)
            self.parent.bind('<Return>', lambda e: self._button_click('='))
            self.parent.bind('<BackSpace>', lambda e: self._button_click('⌫'))
            self.parent.bind('<Escape>', lambda e: self._button_click('C'))

    def _handle_keypress(self, event):
        if event.char.isdigit() or event.char in ['.', '+', '-', '*', '/', '(', ')']:
            self._button_click(event.char)
        elif event.char == '\r':
            self._button_click('=')

    def _button_click(self, button_text):
        current = self.current_number.get()
        
        if button_text in '0123456789.':
            if self.last_was_operator:
                current = button_text
            else:
                current = current + button_text if current != "0" else button_text
            self.last_was_operator = False
            
        elif button_text in ['+', '-', '×', '÷']:
            self.expression.append(float(current))
            self.expression.append(button_text)
            self.last_was_operator = True
            
        elif button_text == '=':
            self.expression.append(float(current))
            result = self._calculate_expression()
            current = str(result)
            self.expression = []
            self.last_was_operator = True
            
        elif button_text == 'C':
            current = "0"
            self.expression = []
            self.last_was_operator = False
            
        elif button_text == '⌫':
            current = current[:-1] if len(current) > 1 else "0"
            
        elif button_text in ['sin', 'cos', 'tan']:
            value = float(current)
            result = self.calc.trig_function(value, button_text)
            current = str(result)
            self.last_was_operator = True
            
        elif button_text == '√':
            value = float(current)
            result = self.calc.advanced_operation(value, 'sqrt')
            current = str(result)
            self.last_was_operator = True
            
        elif button_text == 'x²':
            value = float(current)
            result = self.calc.advanced_operation(value, 'square')
            current = str(result)
            self.last_was_operator = True
            
        elif button_text == '±':
            value = float(current)
            result = self.calc.advanced_operation(value, 'negate')
            current = str(result)
            
        elif button_text == '%':
            value = float(current)
            result = self.calc.advanced_operation(value, 'percent')
            current = str(result)
            self.last_was_operator = True
            
        elif button_text == 'π':
            current = str(math.pi)
            self.last_was_operator = True
            
        elif button_text in ['MC', 'MR', 'MS', 'M+', 'M-']:
            value = float(current)
            result = self.calc.memory_operation(button_text, value)
            if result is not None:  # MR operation
                current = str(result)
            
        elif button_text == 'deg':
            self.calc.toggle_angle_mode()
            button_text = 'rad' if not self.calc.is_degree_mode else 'deg'
            
        self.current_number.set(current)

    def _calculate_expression(self):
        if not self.expression:
            return 0
            
        # Convert × and ÷ to * and /
        ops = {
            '×': '*',
            '÷': '/'
        }
        expression = []
        for item in self.expression:
            if isinstance(item, str) and item in ops:
                expression.append(ops[item])
            else:
                expression.append(item)
                
        # Calculate result
        try:
            result = expression[0]
            for i in range(1, len(expression), 2):
                operator = expression[i]
                operand = expression[i + 1]
                result = self.calc.basic_operation(result, operand, operator)
            return result
        except Exception as e:
            return "Error"
