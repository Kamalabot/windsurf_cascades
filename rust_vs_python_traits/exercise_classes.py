from abc import ABC, abstractmethod
from typing import Any


class Animal(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @abstractmethod
    def make_sound(self) -> str:
        pass

    def describe(self) -> str:
        return f"This is an animal that makes the sound: {self.make_sound()}"


class Dog(Animal):
    def make_sound(self) -> str:
        return f"Woof! My name is {self.name}"

    def __str__(self) -> str:
        return f"Dog {self.name} is {self.age} years old"

    def __repr__(self) -> str:
        return f"Dog(name='{self.name}', age={self.age})"

    def __eq__(self, other: Any) -> bool | Any:
        if not isinstance(other, type(self)):
            # print("getting in heree")
            return NotImplemented
        return self.name == other.name and self.age == other.age

    def __add__(self, other: "Dog") -> int:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.age + other.age

    def __copy__(self):
        return Dog(self.name, self.age)

    @staticmethod
    def from_tuple(tuple_data: tuple[str, int]) -> "Dog":
        return Dog(tuple_data[0], tuple_data[1])


class Cat(Animal):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

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

    def __add__(self, other: "Cat") -> int:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.age + other.age

    def __copy__(self):
        return Cat(self.name, self.age)

    @staticmethod
    def from_tuple(tuple_data: tuple[str, int]) -> "Cat":
        return Cat(tuple_data[0], tuple_data[1])


class Shelter:
    def __init__(self):
        self.animals: list[Animal] = []

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def describe_animals(self):
        for animal in self.animals:
            print(animal.describe())
