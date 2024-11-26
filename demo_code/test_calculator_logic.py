import pytest
import math
from calculator_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_basic_operations(calculator):
    assert calculator.basic_operation(2, 3, '+') == 5
    assert calculator.basic_operation(5, 3, '-') == 2
    assert calculator.basic_operation(4, 3, '*') == 12
    assert calculator.basic_operation(6, 2, '/') == 3
    assert calculator.basic_operation(5, 0, '/') == float('inf')
    
    with pytest.raises(ValueError):
        calculator.basic_operation(1, 1, '%')

def test_advanced_operations(calculator):
    assert calculator.advanced_operation(16, 'sqrt') == 4
    assert calculator.advanced_operation(3, 'square') == 9
    assert calculator.advanced_operation(50, 'percent') == 0.5
    assert calculator.advanced_operation(5, 'negate') == -5
    assert math.isnan(calculator.advanced_operation(-1, 'sqrt'))
    
    with pytest.raises(ValueError):
        calculator.advanced_operation(1, 'invalid')

def test_trigonometric_functions_degrees(calculator):
    calculator.is_degree_mode = True
    assert round(calculator.trig_function(30, 'sin'), 2) == 0.5
    assert round(calculator.trig_function(60, 'cos'), 2) == 0.5
    assert round(calculator.trig_function(45, 'tan'), 2) == 1.0
    
    # Test inverse functions
    assert round(calculator.trig_function(0.5, 'asin'), 2) == 30.0
    assert round(calculator.trig_function(0.5, 'acos'), 2) == 60.0
    assert round(calculator.trig_function(1.0, 'atan'), 2) == 45.0

def test_trigonometric_functions_radians(calculator):
    calculator.is_degree_mode = False
    assert round(calculator.trig_function(math.pi/6, 'sin'), 2) == 0.5
    assert round(calculator.trig_function(math.pi/3, 'cos'), 2) == 0.5
    assert round(calculator.trig_function(math.pi/4, 'tan'), 2) == 1.0

def test_hyperbolic_functions(calculator):
    assert calculator.trig_function(0, 'sinh') == 0
    assert calculator.trig_function(0, 'cosh') == 1
    assert calculator.trig_function(0, 'tanh') == 0

def test_memory_operations(calculator):
    calculator.memory_operation('MS', 5)
    assert calculator.memory_operation('MR') == 5
    
    calculator.memory_operation('M+', 3)
    assert calculator.memory_operation('MR') == 8
    
    calculator.memory_operation('M-', 2)
    assert calculator.memory_operation('MR') == 6
    
    calculator.memory_operation('MC')
    assert calculator.memory_operation('MR') == 0

def test_angle_mode_toggle(calculator):
    assert calculator.is_degree_mode is True
    calculator.toggle_angle_mode()
    assert calculator.is_degree_mode is False
    calculator.toggle_angle_mode()
    assert calculator.is_degree_mode is True
