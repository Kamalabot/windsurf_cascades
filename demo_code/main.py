import tkinter as tk
from tkinter import ttk
from calculator_ui import CalculatorUI
from geometric_ui import GeometricUI

def main():
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)
    
    # Standard Calculator Tab
    calc_frame = ttk.Frame(notebook)
    CalculatorUI(calc_frame)
    notebook.add(calc_frame, text="Standard")
    
    # Geometric Calculator Tab
    geo_frame = ttk.Frame(notebook)
    GeometricUI(geo_frame)
    notebook.add(geo_frame, text="Geometric")
    
    root.mainloop()

if __name__ == "__main__":
    main()
