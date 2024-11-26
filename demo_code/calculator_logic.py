import math
from typing import Union, Optional

class CalculatorLogic:
    def __init__(self):
        self.memory = 0
        self.last_result = 0
        self.is_degree_mode = True  # True for degrees, False for radians
        
    def _to_radians(self, value: float) -> float:
        """Convert value to radians if in degree mode."""
        return math.radians(value) if self.is_degree_mode else value
    
    def _to_degrees(self, value: float) -> float:
        """Convert value from radians to degrees if in degree mode."""
        return math.degrees(value) if self.is_degree_mode else value

    def basic_operation(self, a: float, b: float, operator: str) -> float:
        """Perform basic arithmetic operations."""
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else float('inf'),
        }
        if operator not in operations:
            raise ValueError(f"Invalid operator: {operator}")
        
        result = operations[operator](a, b)
        self.last_result = result
        return result

    def advanced_operation(self, value: float, operation: str) -> float:
        """Perform advanced mathematical operations."""
        operations = {
            'sqrt': lambda x: math.sqrt(x) if x >= 0 else float('nan'),
            'square': lambda x: x ** 2,
            'percent': lambda x: x / 100,
            'negate': lambda x: -x,
        }
        if operation not in operations:
            raise ValueError(f"Invalid operation: {operation}")
        
        result = operations[operation](value)
        self.last_result = result
        return result

    def trig_function(self, value: float, function: str) -> float:
        """Perform trigonometric operations."""
        trig_funcs = {
            'sin': lambda x: math.sin(self._to_radians(x)),
            'cos': lambda x: math.cos(self._to_radians(x)),
            'tan': lambda x: math.tan(self._to_radians(x)),
            'asin': lambda x: self._to_degrees(math.asin(x)),
            'acos': lambda x: self._to_degrees(math.acos(x)),
            'atan': lambda x: self._to_degrees(math.atan(x)),
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
        }
        if function not in trig_funcs:
            raise ValueError(f"Invalid trigonometric function: {function}")
        
        try:
            result = trig_funcs[function](value)
            self.last_result = result
            return result
        except ValueError as e:
            return float('nan')

    def memory_operation(self, operation: str, value: Optional[float] = None) -> Optional[float]:
        """Perform memory operations."""
        if operation == 'MS':  # Memory Store
            self.memory = value if value is not None else self.last_result
        elif operation == 'MR':  # Memory Recall
            return self.memory
        elif operation == 'MC':  # Memory Clear
            self.memory = 0
        elif operation == 'M+':  # Memory Add
            self.memory += value if value is not None else self.last_result
        elif operation == 'M-':  # Memory Subtract
            self.memory -= value if value is not None else self.last_result
        else:
            raise ValueError(f"Invalid memory operation: {operation}")
        
        return None

    def toggle_angle_mode(self) -> None:
        """Toggle between degrees and radians mode."""
        self.is_degree_mode = not self.is_degree_mode
