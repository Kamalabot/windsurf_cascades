# Python Equivalent of Rust Struct and Trait Example
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from dataclasses import dataclass

# Abstract Base Class (similar to Rust trait)
class Animal(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    @abstractmethod
    def make_sound(self) -> str:
        pass
    
    def describe(self) -> str:
        return f"This is an animal that makes the sound: {self.make_sound()}"

# Concrete class implementing the abstract base class with dunder methods
class Dog(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
    
    def make_sound(self) -> str:
        return f"Woof! My name is {self.name}"
    
    # Similar to Display trait in Rust
    def __str__(self) -> str:
        return f"Dog {self.name} is {self.age} years old"
    
    # Similar to Debug trait in Rust
    def __repr__(self) -> str:
        return f"Dog(name='{self.name}', age={self.age})"
    
    # Similar to PartialEq trait in Rust
    def __eq__(self, other: Any) -> bool | Any:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.age == other.age
    
    # Similar to Add trait in Rust
    def __add__(self, other: 'Dog') -> int:
        if not isinstance(other, Dog):
            return NotImplemented
        return self.age + other.age
    
    # Similar to From trait in Rust
    @classmethod
    def from_tuple(cls, tuple_data: Tuple[str, int]) -> 'Dog':
        return cls(tuple_data[0], tuple_data[1])
    
    # Similar to Clone trait in Rust
    def __copy__(self):
        return Dog(self.name, self.age)

class Cat(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
    
    def make_sound(self) -> str:
        return f"Meow! My name is {self.name}"
    
    def __str__(self) -> str:
        return f"Cat {self.name} is {self.age} years old"
    
    def __repr__(self) -> str:
        return f"Cat(name='{self.name}', age={self.age})"
    
    def __eq__(self, other: Any) -> bool | Any:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.age == other.age

class Shelter:
    def __init__(self):
        self.animals: List[Animal] = []
    
    def add_animal(self, animal: Animal):
        self.animals.append(animal)
    
    def describe_animals(self):
        for animal in self.animals:
            print(animal.describe())

def main():
    # Demonstrate various dunder methods
    dog1 = Dog("Buddy", 3)
    dog2 = Dog("Max", 5)
    cat = Cat("Whiskers", 4)

    # __str__ method (Display trait)
    print("String representation:", str(dog1))
    
    # __repr__ method (Debug trait)
    print("Debug representation:", repr(dog1))
    
    # __eq__ method (PartialEq trait)
    print("Are dogs equal?", dog1 == dog2)
    
    # __add__ method (Add trait)
    print("Sum of dog ages:", dog1 + dog2)
    
    # from_tuple method (From trait)
    dog3 = Dog.from_tuple(("Rex", 2))
    print("Converted dog:", dog3)

    # Original animal shelter demo
    shelter = Shelter()
    shelter.add_animal(dog1)
    shelter.add_animal(cat)
    shelter.describe_animals()

if __name__ == "__main__":
    main()
