"""
Object-Oriented Programming (OOP) in Python
=========================================

This file covers classes, objects, inheritance, encapsulation, and polymorphism.
"""

# =========== CLASSES AND OBJECTS ==========
# 1. Basic class definition
class Dog:
    """A simple class to model a dog."""
    
    # Class variable (shared by all instances)
    species = "Canis familiaris"
    
    # Constructor method (initialize instance variables)
    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age
    
    # Instance method
    def description(self):
        """Return a description of the dog."""
        return f"{self.name} is {self.age} years old"
    
    # Instance method
    def speak(self, sound):
        """Simulate the dog making a sound."""
        return f"{self.name} says {sound}"

# Creating instances (objects) of the class
buddy = Dog("Buddy", 9)
miles = Dog("Miles", 4)

# Accessing attributes
print(f"Buddy's species: {buddy.species}")  # Access a class variable
print(f"Buddy's name: {buddy.name}")        # Access an instance variable

# Calling methods
print(buddy.description())
print(buddy.speak("Woof!"))
print(miles.speak("Bark!"))

# =========== INHERITANCE ==========
# Parent class
class Animal:
    """A simple class to represent animals."""
    
    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age
    
    def make_sound(self):
        """Method to be overridden by subclasses."""
        return "Some generic animal sound"

# Child class (inherits from Animal)
class Cat(Animal):
    """A class representing a cat, inherits from Animal."""
    
    def __init__(self, name, age, color):
        """
        Initialize attributes of the parent class and add a new attribute.
        """
        # Call the parent class's __init__ method
        super().__init__(name, age)
        self.color = color
    
    # Override parent class method
    def make_sound(self):
        """Override the parent class method."""
        return "Meow!"
    
    # Add a new method
    def purr(self):
        """Method specific to cats."""
        return f"{self.name} is purring..."

# Create an instance of Cat
whiskers = Cat("Whiskers", 3, "gray")

# Access inherited attributes
print(f"Cat's name: {whiskers.name}, age: {whiskers.age}")

# Access new attribute
print(f"Cat's color: {whiskers.color}")

# Call overridden method
print(f"Cat's sound: {whiskers.make_sound()}")

# Call new method
print(whiskers.purr())

# =========== MULTIPLE INHERITANCE ==========
class Flyable:
    """A mixin class for flyable things."""
    
    def fly(self):
        """Method to fly."""
        return f"{self.__class__.__name__} is flying..."

class Swimmable:
    """A mixin class for swimmable things."""
    
    def swim(self):
        """Method to swim."""
        return f"{self.__class__.__name__} is swimming..."

class Duck(Animal, Flyable, Swimmable):
    """A duck can both fly and swim."""
    
    def make_sound(self):
        """Override the make_sound method."""
        return "Quack!"

# Create a Duck instance
donald = Duck("Donald", 5)

# Access different methods from multiple inheritance
print(donald.make_sound())  # From Animal (overridden)
print(donald.fly())         # From Flyable
print(donald.swim())        # From Swimmable

# =========== ENCAPSULATION ==========
class BankAccount:
    """A class to represent a bank account with encapsulation."""
    
    def __init__(self, owner, balance=0):
        """Initialize with owner and optional starting balance."""
        self.owner = owner
        self.__balance = balance  # Private attribute (name mangling with double underscore)
    
    def deposit(self, amount):
        """Add money to the account."""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """Withdraw money from the account if funds available."""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        """Getter method for balance."""
        return self.__balance
    
    def __str__(self):
        """String representation of the account."""
        return f"{self.owner}'s account. Balance: ${self.__balance}"

# Create an account
account = BankAccount("Alice", 1000)

# Access public methods and attributes
print(account.owner)
print(account.get_balance())

# Direct access to private attribute will fail or use name mangling
# print(account.__balance)  # This would raise an AttributeError

# Use methods to interact with the account
account.deposit(500)
print(account.get_balance())
account.withdraw(200)
print(account.get_balance())
print(account)  # Uses __str__ method

# =========== POLYMORPHISM ==========
class Shape:
    """Base class for shapes."""
    
    def area(self):
        """Calculate the area of the shape."""
        pass
    
    def perimeter(self):
        """Calculate the perimeter of the shape."""
        pass

class Rectangle(Shape):
    """A class for rectangles."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """A class for circles."""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# Function that demonstrates polymorphism
def print_shape_info(shape):
    """Print information about any shape."""
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.perimeter()}")

# Create shapes
rectangle = Rectangle(5, 10)
circle = Circle(7)

# Use polymorphism
print("\nRectangle:")
print_shape_info(rectangle)

print("\nCircle:")
print_shape_info(circle)

# =========== EXERCISES ==========
"""
Exercise 1: Create a class called Employee with attributes for name, job_title, and salary.
            Add methods to give_raise(percent) and display_info().

Exercise 2: Create a subclass called Manager that inherits from Employee and has an
            additional attribute for department and a method to add_employee(employee).

Exercise 3: Design a system of classes to model different vehicles. Start with a base
            Vehicle class and create at least three subclasses (like Car, Motorcycle, 
            and Truck) with appropriate attributes and methods.

Exercise 4: Create a class with at least three private attributes and appropriate
            getter and setter methods to access and modify them.

Exercise 5: Design a simple library system with classes for Book, Library, and Patron.
            Think about the relationships between these classes and what methods and
            attributes each should have.
"""