"""
Functions in Python
=================

This file covers creating and using functions in Python.
"""

# =========== BASIC FUNCTIONS ==========
# 1. Simple function with no parameters
def say_hello():
    """Print a greeting message."""
    print("Hello, World!")

# Calling the function
say_hello()

# 2. Function with parameters
def greet(name):
    """Greet someone by name."""
    print(f"Hello, {name}!")

# Calling the function with an argument
greet("Alice")

# 3. Function with default parameter value
def greet_with_default(name="Guest"):
    """Greet someone by name with a default value."""
    print(f"Hello, {name}!")

# Calling with and without arguments
greet_with_default()  # Uses default value
greet_with_default("Bob")  # Uses provided value

# =========== RETURN VALUES ==========
# 1. Function that returns a value
def square(number):
    """Return the square of a number."""
    return number ** 2

# Calling and using the return value
result = square(5)
print(f"Square of 5 is {result}")

# 2. Function that returns multiple values
def get_min_max(numbers):
    """Return the minimum and maximum values from a list."""
    return min(numbers), max(numbers)

# Unpacking the return values
min_val, max_val = get_min_max([3, 1, 7, 2, 9])
print(f"Minimum: {min_val}, Maximum: {max_val}")

# =========== FUNCTION ARGUMENTS ==========
# 1. Positional arguments
def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f"I have a {animal_type} named {pet_name}.")

# Call with positional arguments (order matters)
describe_pet("hamster", "Harry")

# 2. Keyword arguments
describe_pet(animal_type="cat", pet_name="Whiskers")
describe_pet(pet_name="Rex", animal_type="dog")  # Order doesn't matter

# 3. Variable number of positional arguments (*args)
def add_numbers(*numbers):
    """Sum any number of arguments."""
    return sum(numbers)

# Call with different numbers of arguments
print(f"Sum of 1, 2: {add_numbers(1, 2)}")
print(f"Sum of 1, 2, 3, 4: {add_numbers(1, 2, 3, 4)}")

# 4. Variable number of keyword arguments (**kwargs)
def build_profile(first_name, last_name, **user_info):
    """Build a dictionary with user information."""
    profile = {'first_name': first_name, 'last_name': last_name}
    # Add any other key-value pairs
    profile.update(user_info)
    return profile

# Call with additional keyword arguments
user = build_profile(
    'Albert', 'Einstein',
    field='physics',
    location='Princeton',
    awards=['Nobel Prize'],
    taolaor='mía lao'
)
print(f"User profile: {user}")

# =========== SCOPE OF VARIABLES ==========
# 1. Local and global scope
x = 10  # Global variable

def print_x():
    """Access the global variable."""
    print(f"Global x from function: {x}")

def change_local_x():
    """Create a local variable with the same name."""
    x = 20  # Local variable, does not affect the global variable
    print(f"Local x inside function: {x}")

def change_global_x():
    """Modify the global variable."""
    global x  # Declare x as global
    x = 30
    print(f"Modified global x inside function: {x}")

# Test variable scope
print(f"Global x before functions: {x}")
print_x()
change_local_x()
print(f"Global x after change_local_x: {x}")
change_global_x()
print(f"Global x after change_global_x: {x}")

# =========== LAMBDA FUNCTIONS ==========
# Anonymous functions defined with the lambda keyword
double = lambda x: x * 2
print(f"Double of 5 using lambda: {double(5)}")

# Useful with functions like map, filter, and sorted
numbers = [1, 5, 3, 9, 2, 6]
squared = list(map(lambda x: x**2, numbers))
print(f"Squared numbers using map and lambda: {squared}")

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers using filter and lambda: {even_numbers}")

# Sort a list of tuples by the second element
pairs = [(1, 'one'), (3, 'three'), (2, 'two'), (4, 'four')]
sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
print(f"Sorted pairs by second element: {sorted_pairs}")

# =========== EXERCISES ==========
"""
Exercise 1: Write a function called is_palindrome that checks if a string is 
            a palindrome (reads the same forward and backward). 
            Test it with words like "radar" and "hello".

Exercise 2: Create a function called calculate_discount that calculates the price 
            after a discount. It should take parameters for original_price and 
            discount_percentage (default to 10%).

Exercise 3: Write a function that takes any number of strings as arguments and 
            returns a single string concatenating them all.

Exercise 4: Create a function that takes a list of numbers and returns a new list 
            containing only the even numbers. Use lambda with filter.

Exercise 5: Write a recursive function to calculate the factorial of a number.
            The factorial of n is n × (n-1) × (n-2) × ... × 1.
"""