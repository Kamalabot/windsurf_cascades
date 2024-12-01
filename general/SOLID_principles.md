# SOLID Principles of Software Engineering

SOLID is an acronym for five design principles intended to make software designs more understandable, flexible, and maintainable.

## 1. Single Responsibility Principle (SRP)
A class should have only one reason to change, meaning it should have only one job or responsibility.

```python
# Bad Example
class User:
    def __init__(self, name: str):
        self.name = name
    
    def get_user_data(self):
        # Gets user data
        pass
    
    def save_to_database(self):
        # Saves to database
        pass
    
    def generate_report(self):
        # Generates report
        pass

# Good Example
class User:
    def __init__(self, name: str):
        self.name = name
    
    def get_user_data(self):
        # Gets user data
        pass

class UserDB:
    def save_user(self, user):
        # Saves to database
        pass

class UserReportGenerator:
    def generate_report(self, user):
        # Generates report
        pass
```

## 2. Open-Closed Principle (OCP)
Software entities should be open for extension but closed for modification.

```python
# Bad Example
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class AreaCalculator:
    def calculate_area(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        # Adding new shapes requires modifying this class

# Good Example
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def calculate_area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_area(self):
        return 3.14 * self.radius ** 2
```

## 3. Liskov Substitution Principle (LSP)
Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

```python
# Bad Example
class Bird:
    def fly(self):
        pass

class Penguin(Bird):  # Penguins can't fly!
    def fly(self):
        raise Exception("I can't fly")

# Good Example
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class SwimmingBird(Bird):
    def move(self):
        return "Swimming"
```

## 4. Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use.

```python
# Bad Example
class Worker:
    def work(self):
        pass
    
    def eat(self):
        pass
    
    def sleep(self):
        pass

# Good Example
class Workable:
    def work(self):
        pass

class Eatable:
    def eat(self):
        pass

class Sleepable:
    def sleep(self):
        pass

class Human(Workable, Eatable, Sleepable):
    pass

class Robot(Workable):
    pass
```

## 5. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both should depend on abstractions.

```python
# Bad Example
class MySQLDatabase:
    def save(self, data):
        # Saves to MySQL
        pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Direct dependency on MySQLDatabase
    
    def save_user(self, user):
        self.db.save(user)

# Good Example
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        # Saves to MySQL
        pass

class PostgresDatabase(Database):
    def save(self, data):
        # Saves to Postgres
        pass

class UserService:
    def __init__(self, database: Database):
        self.db = database  # Depends on abstraction
    
    def save_user(self, user):
        self.db.save(user)
```

## Benefits of SOLID Principles

### 1. Maintainability
Maintainability refers to how easy it is to modify, update, and manage code over time. Good maintainability means:
- **Easier Bug Fixes**: When code is well-organized and follows single responsibility, bugs are easier to locate and fix
- **Simpler Updates**: Adding new features or modifying existing ones requires minimal changes to existing code
- **Reduced Technical Debt**: Well-structured code prevents the accumulation of "quick fixes" that can make future changes harder
- **Better Documentation**: Code that follows SOLID principles is self-documenting and easier to understand
- **Lower Maintenance Costs**: Less time and effort required for ongoing maintenance and updates

### 2. Readability
Code is more organized and clearer to understand

### 3. Flexibility
Makes the code more modular and easier to extend

### 4. Testability
Easier to write unit tests

### 5. Reusability
Code components can be reused more effectively

Remember that while these principles are important guidelines, they should be applied with pragmatism. Not every piece of code needs to strictly follow all SOLID principles - the goal is to create maintainable, understandable, and flexible code that serves its purpose effectively.
