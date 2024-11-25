use std::cmp::PartialEq;
use std::convert::From;
use std::fmt;
use std::ops::Add;

trait Animal {
    fn make_sound(&self) -> String;
    fn describe(&self) -> String {
        format!(
            "This is an animal that makes the sound: {}",
            self.make_sound()
        )
    }
}

#[derive(Debug, Clone)]
struct Dog {
    name: String,
    age: u8,
}

impl Add for Dog {
    type Output = u8;
    fn add(self, other: Dog) -> u8 {
        self.age + other.age
    }
}
impl From<(String, u8)> for Dog {
    fn from(tuple: (String, u8)) -> Self {
        Dog::new(tuple.0, tuple.1)
    }
}

impl Dog {
    fn new(name: String, age: u8) -> Self {
        Dog { name, age }
    }
}

impl fmt::Display for Dog {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Dog {} is {} years old", self.name, self.age)
    }
}

impl Animal for Dog {
    fn make_sound(&self) -> String {
        format!("Woof! My name is {}", self.name)
    }
}

impl PartialEq for Dog {
    fn eq(&self, other: &Dog) -> bool {
        self.name == other.name && self.age == other.age
    }
}

#[derive(Debug, Clone)]
struct Cat {
    name: String,
    age: u8,
}

impl Cat {
    fn new(name: String, age: u8) -> Self {
        Cat { name, age }
    }
}

impl Animal for Cat {
    fn make_sound(&self) -> String {
        format!("Meow! My name is {}", self.name)
    }
}

impl fmt::Display for Cat {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Cat {} is {} years old", self.name, self.age)
    }
}

impl PartialEq for Cat {
    fn eq(&self, other: &Cat) -> bool {
        self.name == other.name && self.age == other.age
    }
}

struct Shelter {
    animals: Vec<Box<dyn Animal>>,
}

impl Shelter {
    fn new() -> Self {
        Shelter {
            animals: Vec::new(),
        }
    }
    fn add_animal(&mut self, animal: Box<dyn Animal>) {
        self.animals.push(animal);
    }
}

fn main() {
    // Demonstrate various trait implementations
    println!("Compare Traits with Python Methods..")
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_display_trait() {
        let dog = Dog::new("Buddy".to_owned(), 3);
        assert_eq!(dog.to_string(), "Dog Buddy is 3 years old");
    }

    #[test]
    fn test_debug_trait() {
        let dog = Dog::new(String::from("Buddy"), 3);
        assert_eq!(format!("{:?}", dog), "Dog { name: \"Buddy\", age: 3 }");
    }

    #[test]
    fn test_partial_eq_trait() {
        let dog1 = Dog::new(String::from("Buddy"), 3);
        let dog2 = Dog::new(String::from("Buddy"), 3);
        let dog3 = Dog::new(String::from("Max"), 5);
        assert!(dog1 == dog2);
        assert!(dog1 != dog3);
    }

    #[test]
    fn test_add_trait() {
        let dog1 = Dog::new(String::from("Buddy"), 3);
        let dog2 = Dog::new(String::from("Max"), 5);
        assert_eq!((dog1.clone() + dog2), 8);
    }

    #[test]
    fn test_from_trait() {
        let dog: Dog = (String::from("Rex"), 2).into();
        assert_eq!(dog.name, "Rex");
        assert_eq!(dog.age, 2);
    }

    #[test]
    fn test_animal_trait() {
        let dog = Dog::new(String::from("Buddy"), 3);
        let cat = Cat::new(String::from("Whiskers"), 4);
        assert_eq!(dog.make_sound(), "Woof! My name is Buddy");
        assert_eq!(cat.make_sound(), "Meow! My name is Whiskers");
    }

    #[test]
    fn test_shelter() {
        let mut shelter = Shelter::new();
        let dog = Dog::new(String::from("Buddy"), 3);
        let cat = Cat::new(String::from("Whiskers"), 4);
        shelter.add_animal(Box::new(dog));
        shelter.add_animal(Box::new(cat));
        let animals = shelter
            .animals
            .iter()
            .map(|animal| animal.describe())
            .collect::<Vec<String>>();
        assert_eq!(
            animals,
            vec![
                "This is an animal that makes the sound: Woof! My name is Buddy".to_string(),
                "This is an animal that makes the sound: Meow! My name is Whiskers".to_string()
            ]
        );
    }
}
