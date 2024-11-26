import tkinter as tk
from tkinter import ttk, messagebox
from geometric_calculator import GeometricCalculator

class GeometricUI:
    def __init__(self, parent):
        self.parent = parent
        self.calc = GeometricCalculator()
        
        # If parent is root window, set title
        if isinstance(parent, tk.Tk):
            parent.title("Geometric Calculator")
        
        self.shape_frames = {}
        self.current_frame = None
        
        self._create_main_ui()
        
    def _create_main_ui(self):
        # Create shape selection frame
        selection_frame = ttk.LabelFrame(self.parent, text="Select Shape", padding="10")
        selection_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        shapes = [
            ("Circle", self._create_circle_frame),
            ("Rectangle", self._create_rectangle_frame),
            ("Triangle", self._create_triangle_frame),
            ("Sphere", self._create_sphere_frame),
            ("Cylinder", self._create_cylinder_frame),
            ("Cone", self._create_cone_frame),
            ("Cube", self._create_cube_frame)
        ]
        
        for i, (shape, frame_creator) in enumerate(shapes):
            btn = ttk.Button(
                selection_frame,
                text=shape,
                command=lambda fc=frame_creator: self._switch_frame(fc)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Create result frame
        self.result_var = tk.StringVar(value="Result: ")
        result_label = ttk.Label(
            self.parent,
            textvariable=self.result_var,
            font=('Arial', 12)
        )
        result_label.grid(row=2, column=0, pady=10)
        
    def _switch_frame(self, frame_creator):
        if self.current_frame:
            self.current_frame.grid_remove()
        
        if frame_creator not in self.shape_frames:
            self.shape_frames[frame_creator] = frame_creator()
            
        self.current_frame = self.shape_frames[frame_creator]
        self.current_frame.grid(row=1, column=0, padx=10, pady=5)
        
    def _create_entry_with_label(self, parent, label_text):
        frame = ttk.Frame(parent)
        label = ttk.Label(frame, text=label_text)
        label.grid(row=0, column=0, padx=5)
        entry = ttk.Entry(frame)
        entry.grid(row=0, column=1, padx=5)
        return frame, entry
        
    def _create_circle_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Circle", padding="10")
        
        radius_frame, radius_entry = self._create_entry_with_label(frame, "Radius:")
        radius_frame.grid(row=0, column=0, pady=5)
        
        def calculate():
            try:
                r = float(radius_entry.get())
                area = self.calc.circle_area(r)
                perimeter = self.calc.circle_perimeter(r)
                self.result_var.set(f"Area: {area:.2f}, Perimeter: {perimeter:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=1, column=0, pady=10)
        return frame
        
    def _create_rectangle_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Rectangle", padding="10")
        
        length_frame, length_entry = self._create_entry_with_label(frame, "Length:")
        length_frame.grid(row=0, column=0, pady=5)
        
        width_frame, width_entry = self._create_entry_with_label(frame, "Width:")
        width_frame.grid(row=1, column=0, pady=5)
        
        def calculate():
            try:
                l = float(length_entry.get())
                w = float(width_entry.get())
                area = self.calc.rectangle_area(l, w)
                perimeter = self.calc.rectangle_perimeter(l, w)
                self.result_var.set(f"Area: {area:.2f}, Perimeter: {perimeter:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=2, column=0, pady=10)
        return frame
        
    def _create_triangle_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Triangle", padding="10")
        
        base_frame, base_entry = self._create_entry_with_label(frame, "Base:")
        base_frame.grid(row=0, column=0, pady=5)
        
        height_frame, height_entry = self._create_entry_with_label(frame, "Height:")
        height_frame.grid(row=1, column=0, pady=5)
        
        sides_label = ttk.Label(frame, text="For Perimeter:")
        sides_label.grid(row=2, column=0, pady=5)
        
        side_frames = []
        side_entries = []
        for i in range(3):
            frame_side, entry = self._create_entry_with_label(frame, f"Side {i+1}:")
            frame_side.grid(row=3+i, column=0, pady=5)
            side_frames.append(frame_side)
            side_entries.append(entry)
        
        def calculate():
            try:
                b = float(base_entry.get())
                h = float(height_entry.get())
                area = self.calc.triangle_area(b, h)
                
                sides = [float(entry.get()) for entry in side_entries]
                perimeter = self.calc.triangle_perimeter(*sides)
                
                self.result_var.set(f"Area: {area:.2f}, Perimeter: {perimeter:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=6, column=0, pady=10)
        return frame
        
    def _create_sphere_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Sphere", padding="10")
        
        radius_frame, radius_entry = self._create_entry_with_label(frame, "Radius:")
        radius_frame.grid(row=0, column=0, pady=5)
        
        def calculate():
            try:
                r = float(radius_entry.get())
                volume = self.calc.sphere_volume(r)
                self.result_var.set(f"Volume: {volume:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=1, column=0, pady=10)
        return frame
        
    def _create_cylinder_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Cylinder", padding="10")
        
        radius_frame, radius_entry = self._create_entry_with_label(frame, "Radius:")
        radius_frame.grid(row=0, column=0, pady=5)
        
        height_frame, height_entry = self._create_entry_with_label(frame, "Height:")
        height_frame.grid(row=1, column=0, pady=5)
        
        def calculate():
            try:
                r = float(radius_entry.get())
                h = float(height_entry.get())
                volume = self.calc.cylinder_volume(r, h)
                self.result_var.set(f"Volume: {volume:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=2, column=0, pady=10)
        return frame
        
    def _create_cone_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Cone", padding="10")
        
        radius_frame, radius_entry = self._create_entry_with_label(frame, "Radius:")
        radius_frame.grid(row=0, column=0, pady=5)
        
        height_frame, height_entry = self._create_entry_with_label(frame, "Height:")
        height_frame.grid(row=1, column=0, pady=5)
        
        def calculate():
            try:
                r = float(radius_entry.get())
                h = float(height_entry.get())
                volume = self.calc.cone_volume(r, h)
                self.result_var.set(f"Volume: {volume:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=2, column=0, pady=10)
        return frame
        
    def _create_cube_frame(self):
        frame = ttk.LabelFrame(self.parent, text="Cube", padding="10")
        
        side_frame, side_entry = self._create_entry_with_label(frame, "Side Length:")
        side_frame.grid(row=0, column=0, pady=5)
        
        def calculate():
            try:
                s = float(side_entry.get())
                volume = self.calc.cube_volume(s)
                self.result_var.set(f"Volume: {volume:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(frame, text="Calculate", command=calculate).grid(row=1, column=0, pady=10)
        return frame
