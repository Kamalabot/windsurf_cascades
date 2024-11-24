# Rust vs Python: Structs, Traits, and Object-Oriented Programming

## Overview
This project demonstrates the similarities and differences between Rust's struct/trait system and Python's class-based object-oriented programming, with a focus on common traits and their Python dunder method equivalents.

## Trait and Dunder Method Comparisons

### 1. String Representation
- **Rust**: `Display` trait (`fmt::Display`)
  ```rust
  impl fmt::Display for Dog {
      fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result
  }
  ```
- **Python**: `__str__` dunder method
  ```python
  def __str__(self) -> str
  ```

### 2. Debug Representation
- **Rust**: `Debug` trait (derived with `#[derive(Debug)]`)
- **Python**: `__repr__` dunder method

### 3. Equality Comparison
- **Rust**: `PartialEq` trait
  ```rust
  impl PartialEq for Dog {
      fn eq(&self, other: &Self) -> bool
  }
  ```
- **Python**: `__eq__` dunder method
  ```python
  def __eq__(self, other: Any) -> bool
  ```

### 4. Arithmetic Operations
- **Rust**: `Add`, `Sub`, etc. traits from `std::ops`
  ```rust
  impl std::ops::Add for Dog {
      type Output = u8;
      fn add(self, other: Self) -> Self::Output
  }
  ```
- **Python**: `__add__`, `__sub__`, etc. dunder methods
  ```python
  def __add__(self, other: 'Dog') -> int
  ```

### 5. Type Conversion
- **Rust**: `From` and `Into` traits
  ```rust
  impl From<(String, u8)> for Dog {
      fn from(tuple: (String, u8)) -> Self
  }
  ```
- **Python**: Class methods or `__init__` overloads
  ```python
  @classmethod
  def from_tuple(cls, tuple_data: Tuple[str, int]) -> 'Dog'
  ```

### 6. Cloning/Copying
- **Rust**: `Clone` trait (derived with `#[derive(Clone)]`)
- **Python**: `__copy__` dunder method

## Key Differences
1. **Trait Implementation**
   - Rust requires explicit trait implementation in separate `impl` blocks
   - Python defines methods directly within the class

2. **Type Safety**
   - Rust enforces type safety at compile time
   - Python performs type checking at runtime

3. **Memory Management**
   - Rust uses ownership and borrowing rules
   - Python uses garbage collection

4. **Method Resolution**
   - Rust uses static dispatch by default (monomorphization)
   - Python uses dynamic dispatch

## Running the Examples
### Rust
```bash
cargo run
```

### Python
```bash
python python_comparison.py
```

## Learning Objectives
- Understand how Rust traits map to Python dunder methods
- Learn about type conversion and operator overloading in both languages
- Explore different approaches to object-oriented programming
- Compare static vs dynamic typing approaches

## Recommended Reading
- [Rust Book - Traits](https://doc.rust-lang.org/book/ch10-02-traits.html)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Rust std::ops Documentation](https://doc.rust-lang.org/std/ops/index.html)
- [Python Special Methods](https://docs.python.org/3/reference/datamodel.html#special-method-names)
