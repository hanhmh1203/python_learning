"""
Python Basics: Introduction to Python
====================================

This file covers the basic concepts of Python programming.
"""

# =========== PRINT AND COMMENTS ==========
# This is a comment in Python
print("Hello, World!")  # Print a string to the console

# =========== VARIABLES AND DATA TYPES ==========
# 1. Integers
age = 25
print(f"Age: {age}, Type: {type(age)}")

# 2. Floating-point numbers
height = 1.75
print(f"Height: {height}, Type: {type(height)}")

# 3. Strings
name = "Python Learner"
print(f"Name: {name}, Type: {type(name)}")
name = 21111
print(f"Name int: {name}, Type: {type(name)}")

# String operations
print(f"Uppercase: {name.upper()}")
print(f"Length: {len(name)}")
print(f"Contains 'thon': {'thon' in name}")

# 4. Booleans
is_student = True
print(f"Is Student: {is_student}, Type: {type(is_student)}")

# 5. None type
no_value = None
print(f"No Value: {no_value}, Type: {type(no_value)}")

# =========== BASIC OPERATIONS ==========
# Arithmetic operations
a, b = 10, 3
print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")
print(f"Division: {a / b}")
print(f"Floor Division: {a // b}")
print(f"Modulus: {a % b}")
print(f"Exponentiation: {a ** b}")

# =========== TYPE CONVERSION ==========
# Converting between types
string_number = "42"
converted_number = int(string_number)
print(f"String to Int: {string_number} → {converted_number}")

float_number = 3.14159
converted_int = int(float_number)
print(f"Float to Int: {float_number} → {converted_int}")

number = 100
converted_string = str(number)
print(f"Number to String: {number} → {converted_string}")

# =========== USER INPUT ==========
# Uncomment the line below to try it out
# user_input = input("Enter something: ")
# print(f"You entered: {user_input}")

# =========== EXERCISES ==========
"""
Exercise 1: Create variables for your name, age, and favorite programming language.
            Print a sentence that includes all three variables.

Exercise 2: Calculate the area of a circle with radius 5. Use the formula: area = π * r²
            (You may use 3.14159 for π or import math and use math.pi)
            
Exercise 3: Convert a temperature from Fahrenheit to Celsius using the formula:
            C = (F - 32) * 5/9
            Test it with 98.6°F
"""