import pytest
from exercise_classes import Dog, Cat, Shelter

# from python_comparison import Dog, Cat, Shelter


def test_str_method():
    dog = Dog("Buddy", 3)
    assert str(dog) == "Dog Buddy is 3 years old"


def test_repr_method():
    dog = Dog("Buddy", 3)
    assert repr(dog) == "Dog(name='Buddy', age=3)"


def test_eq_method():
    dog1 = Dog("Buddy", 3)
    dog2 = Dog("Buddy", 3)
    dog3 = Dog("Max", 5)
    assert (dog1 == dog2) is True
    assert (dog1 == dog3) is False


def test_add_method():
    dog1 = Dog("Buddy", 3)
    dog2 = Dog("Max", 5)
    assert (dog1 + dog2) == 8


def test_from_tuple():
    dog = Dog.from_tuple(("Rex", 2))
    assert dog.name == "Rex"
    assert dog.age == 2


def test_animal_interface():
    dog = Dog("Buddy", 3)
    cat = Cat("Whiskers", 4)
    assert dog.make_sound() == "Woof! My name is Buddy"
    assert cat.make_sound() == "Meow! My name is Whiskers"


def test_shelter():
    shelter = Shelter()
    dog = Dog("Buddy", 3)
    cat = Cat("Whiskers", 4)
    shelter.add_animal(dog)
    shelter.add_animal(cat)
    animals = [animal.describe() for animal in shelter.animals]
    assert animals == [
        "This is an animal that makes the sound: Woof! My name is Buddy",
        "This is an animal that makes the sound: Meow! My name is Whiskers",
    ]


def test_copy():
    dog1 = Dog("Buddy", 3)
    dog2 = dog1.__copy__()
    assert dog1 == dog2
    assert dog1 is not dog2  # Ensure it's a new object


# Test error cases
def test_add_with_invalid_type():
    dog = Dog("Buddy", 3)
    with pytest.raises(TypeError):
        _ = dog + "invalid"


def test_eq_with_invalid_type():
    dog = Dog("Buddy", 3)
    assert (dog == "invalid") is False
