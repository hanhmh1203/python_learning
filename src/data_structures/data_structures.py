"""
Data Structures in Python
========================

This file covers the main data structures in Python: lists, tuples, dictionaries, and sets.
"""

# =========== LISTS ==========
print("===== LISTS =====")
# Lists are ordered, mutable collections that can contain items of different types
# Creating lists
fruits = ["apple", "banana", "cherry", "orange", "kiwi"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]

# Accessing list elements (indexing)
print(f"First fruit: {fruits[0]}")  # First element (starts at 0)
print(f"Last fruit: {fruits[-1]}")  # Negative indexing for elements from the end

# Slicing lists
print(f"First three fruits: {fruits[0:3]}")  # Elements from index 0 to 2
print(f"All fruits except first two: {fruits[2:]}")  # Elements from index 2 to end
print(f"Last three fruits: {fruits[-3:]}")  # Last three elements

# List operations
print(f"Length of fruits list: {len(fruits)}")  # Number of elements
fruits.append("mango")  # Add an item to the end
print(f"After append: {fruits}")

fruits.insert(1, "avocado")  # Insert an item at a specific position
print(f"After insert: {fruits}")

fruits.remove("banana")  # Remove a specific item
print(f"After remove: {fruits}")

popped_fruit = fruits.pop()  # Remove and return the last item
print(f"Popped fruit: {popped_fruit}")
print(f"After pop: {fruits}")

fruits.sort()  # Sort the list in place
print(f"After sort: {fruits}")

fruits.reverse()  # Reverse the list in place
print(f"After reverse: {fruits}")

# List comprehensions
squares = [x**2 for x in range(1, 6)]
print(f"Squares using list comprehension: {squares}")

even_numbers = [x for x in range(1, 11) if x % 2 == 0]
print(f"Even numbers using list comprehension: {even_numbers}")

# =========== TUPLES ==========
print("\n===== TUPLES =====")
# Tuples are ordered, immutable collections
# Creating tuples
coordinates = (10, 20)
person = ("John", 25, "Developer")
single_item_tuple = (42,)  # Comma is necessary for single-item tuples

# Accessing tuple elements
print(f"X coordinate: {coordinates[0]}")
print(f"Person name: {person[0]}")

# Tuple operations
print(f"Length of person tuple: {len(person)}")
print(f"Count of 'John' in person: {person.count('John')}")
print(f"Index of 25 in person: {person.index(25)}")

# Tuple unpacking
name, age, job = person  # Unpack the tuple into variables
print(f"Name: {name}, Age: {age}, Job: {job}")

# =========== DICTIONARIES ==========
print("\n===== DICTIONARIES =====")
# Dictionaries are unordered, mutable collections of key-value pairs
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "job": "Engineer",
    "skills": ["Python", "SQL", "JavaScript"]
}

# Accessing dictionary values
print(f"Name: {person['name']}")
print(f"Skills: {person['skills']}")
print(f"First skill: {person['skills'][0]}")

# Alternative access with get() (provides default if key doesn't exist)
print(f"Salary (with default): {person.get('salary', 'Not specified')}")

# Adding or modifying items
person["location"] = "New York"  # Add a new key-value pair
person["age"] = 31  # Modify an existing value
print(f"After updates: {person}")

# Dictionary operations
print(f"Dictionary keys: {list(person.keys())}")
print(f"Dictionary values: {list(person.values())}")
print(f"Dictionary items: {list(person.items())}")

# Dictionary comprehensions
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"Squares dictionary: {squares_dict}")

# =========== SETS ==========
print("\n===== SETS =====")
# Sets are unordered, mutable collections of unique elements
# Creating sets
fruits_set = {"apple", "banana", "cherry"}
numbers_set = {1, 2, 3, 4, 5}

# Adding elements
fruits_set.add("orange")
print(f"After add: {fruits_set}")

# Removing elements
fruits_set.remove("banana")  # Raises error if element doesn't exist
print(f"After remove: {fruits_set}")

fruits_set.discard("mango")  # No error if element doesn't exist
print(f"After discard of non-existent element: {fruits_set}")

# Set operations
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"Union: {set_a | set_b}")  # Elements in either set
print(f"Intersection: {set_a & set_b}")  # Elements in both sets
print(f"Difference (A-B): {set_a - set_b}")  # Elements in A but not in B
print(f"Symmetric difference: {set_a ^ set_b}")  # Elements in either set but not both

# Set comprehensions
even_set = {x for x in range(10) if x % 2 == 0}
print(f"Even numbers set: {even_set}")

# =========== EXERCISES ==========
"""
Exercise 1: Create a list of your favorite movies. Then add a new movie, remove one,
            and print the list sorted alphabetically.

Exercise 2: Create a dictionary representing a person with keys for name, age, city, 
            and hobbies (a list). Print each piece of information with appropriate labels.

Exercise 3: Create two sets of numbers and perform union, intersection, and difference 
            operations on them. Interpret the results.

Exercise 4: Write a function that takes a list of numbers and returns a tuple containing 
            (minimum, maximum, sum, average).

Exercise 5: Create a dictionary where the keys are names and the values are ages. 
            Use a dictionary comprehension to create a new dictionary with only people 
            who are 18 or older.
"""