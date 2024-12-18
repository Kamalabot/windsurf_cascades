use wasm_bindgen::prelude::*;
use std::f64::consts::PI;

#[wasm_bindgen]
pub struct Calculator {
    memory: f64,
    current_value: f64,
    previous_value: Option<f64>,
    operation: Option<String>,
    use_radians: bool,
}

#[wasm_bindgen]
impl Calculator {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Calculator {
            memory: 0.0,
            current_value: 0.0,
            previous_value: None,
            operation: None,
            use_radians: true,
        }
    }

    pub fn add(&mut self, value: f64) -> f64 {
        if let Some(prev) = self.previous_value {
            self.current_value = prev + self.current_value;
        }
        self.previous_value = Some(value);
        self.operation = Some(String::from("+"));
        self.current_value
    }

    pub fn subtract(&mut self, value: f64) -> f64 {
        if let Some(prev) = self.previous_value {
            self.current_value = prev - self.current_value;
        }
        self.previous_value = Some(value);
        self.operation = Some(String::from("-"));
        self.current_value
    }

    pub fn multiply(&mut self, value: f64) -> f64 {
        if let Some(prev) = self.previous_value {
            self.current_value = prev * self.current_value;
        }
        self.previous_value = Some(value);
        self.operation = Some(String::from("*"));
        self.current_value
    }

    pub fn divide(&mut self, value: f64) -> Result<f64, JsValue> {
        if value == 0.0 {
            return Err(JsValue::from_str("Division by zero"));
        }
        if let Some(prev) = self.previous_value {
            self.current_value = prev / self.current_value;
        }
        self.previous_value = Some(value);
        self.operation = Some(String::from("/"));
        Ok(self.current_value)
    }

    pub fn equals(&mut self) -> f64 {
        if let (Some(prev), Some(op)) = (self.previous_value, self.operation.as_deref()) {
            self.current_value = match op {
                "+" => prev + self.current_value,
                "-" => prev - self.current_value,
                "*" => prev * self.current_value,
                "/" => if self.current_value != 0.0 { prev / self.current_value } else { self.current_value },
                _ => self.current_value,
            };
        }
        self.previous_value = None;
        self.operation = None;
        self.current_value
    }

    pub fn clear(&mut self) {
        self.current_value = 0.0;
        self.previous_value = None;
        self.operation = None;
    }

    pub fn get_current_value(&self) -> f64 {
        self.current_value
    }

    pub fn set_value(&mut self, value: f64) {
        self.current_value = value;
    }

    // Memory Functions
    pub fn memory_store(&mut self) {
        self.memory = self.current_value;
    }

    pub fn memory_recall(&self) -> f64 {
        self.memory
    }

    pub fn memory_clear(&mut self) {
        self.memory = 0.0;
    }

    pub fn memory_add(&mut self) {
        self.memory += self.current_value;
    }

    pub fn memory_subtract(&mut self) {
        self.memory -= self.current_value;
    }

    // Trigonometric Functions
    pub fn sin(&self, value: f64) -> f64 {
        let angle = if self.use_radians { value } else { value * PI / 180.0 };
        angle.sin()
    }

    pub fn cos(&self, value: f64) -> f64 {
        let angle = if self.use_radians { value } else { value * PI / 180.0 };
        angle.cos()
    }

    pub fn tan(&self, value: f64) -> f64 {
        let angle = if self.use_radians { value } else { value * PI / 180.0 };
        angle.tan()
    }

    pub fn toggle_angle_mode(&mut self) {
        self.use_radians = !self.use_radians;
    }
}
