"""
Control Flow in Python
=====================

This file covers control flow structures in Python including if-else statements and loops.
"""

# =========== CONDITIONAL STATEMENTS ==========
# 1. Simple if statement
x = 10
if x > 5:
    print("x is greater than 5")

# 2. if-else statement
y = 3
if y > 5:
    print("y is greater than 5")
else:
    print("y is not greater than 5")

# 3. if-elif-else statement
z = 5
if z > 10:
    print("z is greater than 10")
elif z == 5:
    print("z is exactly 5")
else:
    print("z is less than 5")

# 4. Nested if statements
a = 15
b = 20
if a > 10:
    print("a is greater than 10")
    if b > 15:
        print("and b is greater than 15")

# 5. Conditional expressions (ternary operator)
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")

# =========== LOOPS ==========
# 1. For loop with a list
print("\nFor loop with a list:")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# 2. For loop with range
print("\nFor loop with range:")
for i in range(5):  # 0 to 4
    print(f"Number: {i}")

# 3. For loop with range (start, stop, step)
print("\nFor loop with range parameters:")
for i in range(2, 10, 4):  # 2, 4, 6, 8
    print(f"Even number: {i}")

# 4. While loop
print("\nWhile loop:")
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# 5. Break statement
print("\nFor loop with break:")
for i in range(10):
    if i == 5:
        print("Breaking the loop at i=5")
        break
    print(f"Number: {i}")

# 6. Continue statement
print("\nFor loop with continue:")
for i in range(7):
    if i % 2 == 0:  # Skip even numbers
        continue
    print(f"Odd number: {i}")

# 7. Else clause with loops
print("\nFor loop with else clause:")
for i in range(3):
    print(f"Item: {i}")
else:
    print("Loop completed successfully")

print("\nFor loop with break and else clause:")
for i in range(3):
    if i == 1:
        break
    print(f"Item: {i}")
else:
    print("This won't execute because the loop was broken")

# =========== EXERCISES ==========
"""
Exercise 1: Write a program that checks if a number is positive, negative, or zero.
            Test it with values: 10, -5, and 0.

Exercise 2: Create a loop that prints the first 10 square numbers (1, 4, 9, 16, ...).

Exercise 3: Write a program that prints the Fibonacci sequence up to the 10th term.
            The Fibonacci sequence starts with 0 and 1, and each subsequent number is
            the sum of the two previous ones (0, 1, 1, 2, 3, 5, 8, 13, ...).

Exercise 4: Create a program that generates a multiplication table for a given number.
            For example, if the number is 5, the program should print:
            5 x 1 = 5
            5 x 2 = 10
            ...
            5 x 10 = 50
"""