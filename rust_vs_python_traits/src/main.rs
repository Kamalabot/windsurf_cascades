use std::fmt;
use std::cmp::PartialEq;
use std::convert::From;

// Basic trait (similar to Python's ABC)
trait Animal {
    fn make_sound(&self) -> String;
    fn describe(&self) -> String {
        format!("This is an animal that makes the sound: {}", self.make_sound())
    }
}

// Struct definition with more complete trait implementations
#[derive(Debug, Clone)]  // Similar to Python's __repr__ and copy functionality
struct Dog {
    name: String,
    age: u8,
}

// Implementation block for Dog-specific methods (similar to regular Python methods)
impl Dog {
    // Constructor (similar to Python's __init__)
    fn new(name: String, age: u8) -> Self {
        Dog { name, age }
    }
}

// Display trait implementation (similar to Python's __str__)
impl fmt::Display for Dog {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Dog {} is {} years old", self.name, self.age)
    }
}

// PartialEq trait implementation (similar to Python's __eq__)
impl PartialEq for Dog {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name && self.age == other.age
    }
}

// Add trait implementation (similar to Python's __add__)
impl std::ops::Add for Dog {
    type Output = u8;

    fn add(self, other: Self) -> Self::Output {
        self.age + other.age
    }
}

// From trait implementation (similar to type conversion in Python)
impl From<(String, u8)> for Dog {
    fn from(tuple: (String, u8)) -> Self {
        Dog::new(tuple.0, tuple.1)
    }
}

// Animal trait implementation
impl Animal for Dog {
    fn make_sound(&self) -> String {
        format!("Woof! My name is {}", self.name)
    }
}

// Cat struct with similar implementations
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

impl fmt::Display for Cat {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Cat {} is {} years old", self.name, self.age)
    }
}

impl PartialEq for Cat {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name && self.age == other.age
    }
}

impl Animal for Cat {
    fn make_sound(&self) -> String {
        format!("Meow! My name is {}", self.name)
    }
}

// Shelter struct remains similar but with added functionality
struct Shelter {
    animals: Vec<Box<dyn Animal>>,
}

impl Shelter {
    fn new() -> Self {
        Shelter { animals: Vec::new() }
    }

    fn add_animal(&mut self, animal: Box<dyn Animal>) {
        self.animals.push(animal);
    }

    fn describe_animals(&self) {
        for animal in &self.animals {
            println!("{}", animal.describe());
        }
    }
}

fn main() {
    // Demonstrate various trait implementations
    let dog1 = Dog::new(String::from("Buddy"), 3);
    let dog2 = Dog::new(String::from("Max"), 5);
    let cat = Cat::new(String::from("Whiskers"), 4);

    // Display trait (str)
    println!("Display trait: {}", dog1);
    
    // Debug trait (repr)
    println!("Debug trait: {:?}", dog1);
    
    // PartialEq trait (eq)
    println!("Are dogs equal? {}", dog1 == dog2);
    
    // Add trait (add)
    println!("Sum of dog ages: {}", dog1.clone() + dog2);
    
    // From trait (conversion)
    let dog3: Dog = (String::from("Rex"), 2).into();
    println!("Converted dog: {}", dog3);

    // Original animal shelter demo
    let mut shelter = Shelter::new();
    shelter.add_animal(Box::new(dog1));
    shelter.add_animal(Box::new(cat));
    shelter.describe_animals();
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_display_trait() {
        let dog = Dog::new(String::from("Buddy"), 3);
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
        assert_eq!(dog1 == dog2, true);
        assert_eq!(dog1 == dog3, false);
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
        let animals = shelter.animals
            .iter()
            .map(|animal| animal.describe())
            .collect::<Vec<String>>();
        assert_eq!(animals, vec![
            "This is an animal that makes the sound: Woof! My name is Buddy".to_string(),
            "This is an animal that makes the sound: Meow! My name is Whiskers".to_string()
        ]);
    }
}
