"""
Error Handling in Python
======================

This file covers handling exceptions, creating custom exceptions, and using
context managers to ensure proper resource cleanup.
"""

# =========== BASIC EXCEPTION HANDLING ==========
print("===== BASIC EXCEPTION HANDLING =====")

# 1. Try and Except
print("\nHandling a ZeroDivisionError:")
try:
    result = 10 / 0
    print(f"Result: {result}")  # This line won't execute
except ZeroDivisionError:
    print("Error: Division by zero")

# 2. Try with multiple except blocks
print("\nHandling different types of exceptions:")
try:
    # Uncomment one of these to test different exceptions
    # num = int("hello")  # ValueError
    # result = 10 / 0     # ZeroDivisionError
    # print(undefined_var)  # NameError
    value = [1, 2, 3][10]  # IndexError
except ValueError:
    print("Error: Invalid conversion")
except ZeroDivisionError:
    print("Error: Division by zero")
except NameError:
    print("Error: Undefined variable")
except Exception as e:
    print(f"Error: {e} (type: {type(e).__name__})")

# 3. The else clause (executed if no exception is raised)
print("\nUsing else clause:")
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error: Division by zero")
else:
    print(f"Division successful, result: {result}")

# 4. The finally clause (always executed)
print("\nUsing finally clause:")
try:
    result = 10 / 2
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Division by zero")
finally:
    print("This will always be executed, regardless of exceptions")

# =========== HANDLING MULTIPLE EXCEPTIONS ==========
print("\n===== HANDLING MULTIPLE EXCEPTIONS =====")

# 1. Catching multiple exceptions in one except block
try:
    # This could cause various exceptions
    value = int(input("Enter a number: "))
    result = 100 / value
    print(f"Result: {result}")
except (ValueError, ZeroDivisionError) as e:
    print(f"Error: {e}")

# =========== RAISING EXCEPTIONS ==========
print("\n===== RAISING EXCEPTIONS =====")

# 1. Raising an exception manually
def validate_age(age):
    """Validate that age is a positive integer."""
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise ValueError("Age cannot be negative")
    return True

# Test the function
try:
    validate_age(-5)
except Exception as e:
    print(f"Caught an exception: {e}")

# 2. Re-raising exceptions
def process_data(data):
    """Process data and handle specific aspects of exceptions."""
    try:
        return data[0] / data[1]
    except Exception as e:
        print(f"An error occurred while processing data: {e}")
        # Add additional info and re-raise
        raise ValueError(f"Invalid data: {data}") from e

# Test the function
try:
    result = process_data([10, 0])
except Exception as e:
    print(f"Outer exception handler: {e}")

# =========== CUSTOM EXCEPTIONS ==========
print("\n===== CUSTOM EXCEPTIONS =====")

# 1. Creating a custom exception class
class InsufficientFundsError(Exception):
    """Exception raised when a withdrawal exceeds the available balance."""
    
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.deficit = amount - balance
        super().__init__(f"Insufficient funds: balance={balance}, amount={amount}, deficit={self.deficit}")

# 2. Using the custom exception
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

# Test the custom exception
account = BankAccount(100)
try:
    account.withdraw(150)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"You need {e.deficit} more funds")

# =========== CONTEXT MANAGERS ==========
print("\n===== CONTEXT MANAGERS (WITH STATEMENT) =====")

# 1. Using with for file handling (automatic cleanup)
print("\nUsing with for file handling:")
try:
    with open("example.txt", "w") as file:
        file.write("This is written using a context manager.\n")
        file.write("The file will be automatically closed.")
    print("File was written and closed automatically")
except Exception as e:
    print(f"Error: {e}")

# Read the file back
with open("example.txt", "r") as file:
    content = file.read()
    print(f"File content: {content}")

# 2. Creating a custom context manager using a class
print("\nCustom context manager using a class:")
class ManagedResource:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"Acquiring resource: {self.name}")
        return self  # Return the resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing resource: {self.name}")
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
            # Return True to suppress the exception, False to propagate it
            return False
    
    def do_something(self):
        print(f"Using resource: {self.name}")

# Test the custom context manager
try:
    with ManagedResource("Database") as resource:
        resource.do_something()
        # Uncomment to test exception handling
        # raise ValueError("Test exception")
    print("ManagedResource context completed")
except Exception as e:
    print(f"Exception caught outside context: {e}")

# 3. Creating a context manager using contextlib
print("\nContext manager using contextlib:")
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Acquiring resource: {name}")
    try:
        # Resource acquisition
        resource = {"name": name, "value": 42}
        yield resource  # Yield the resource
    except Exception as e:
        print(f"Exception inside context manager: {e}")
        raise  # Re-raise the exception
    finally:
        # Resource cleanup (always executed)
        print(f"Releasing resource: {name}")

# Test the contextlib context manager
try:
    with managed_resource("API") as resource:
        print(f"Using resource: {resource['name']}, value: {resource['value']}")
        # Uncomment to test exception handling
        # raise ValueError("Test exception")
    print("contextlib context completed")
except Exception as e:
    print(f"Exception caught outside context: {e}")

# =========== DEBUGGING ASSERTIONS ==========
print("\n===== DEBUGGING ASSERTIONS =====")

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    assert isinstance(numbers, list), "Input must be a list"
    assert len(numbers) > 0, "List cannot be empty"
    assert all(isinstance(x, (int, float)) for x in numbers), "All elements must be numbers"
    
    return sum(numbers) / len(numbers)

# Test the function with assertions
try:
    # Should work
    avg = calculate_average([1, 2, 3, 4, 5])
    print(f"Average: {avg}")
    
    # Should raise an assertion error
    avg = calculate_average([])
    print(f"This won't be printed")
except AssertionError as e:
    print(f"Assertion error caught: {e}")

# =========== EXERCISES ==========
"""
Exercise 1: Write a function that asks the user for two numbers and returns their 
            division. Handle exceptions for division by zero and invalid input.

Exercise 2: Create a custom exception called InvalidEmailError and use it in a function 
            that validates email addresses.

Exercise 3: Write a context manager for a database connection that ensures the 
            connection is always closed properly, even if errors occur.

Exercise 4: Create a program that reads a file and processes its contents. Handle 
            all possible exceptions that might occur, including FileNotFoundError,
            PermissionError, and general I/O errors.

Exercise 5: Implement a retry mechanism that attempts to execute a function multiple 
            times before giving up. Use exception handling to catch errors and decide 
            when to retry.
"""