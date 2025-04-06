"""
File Handling in Python
=====================

This file covers reading from and writing to files, working with different file formats,
and handling file paths.
"""

# =========== READING FILES ==========
# 1. Opening and reading a text file
print("===== BASIC FILE READING =====")

# Create a sample text file to work with
with open("sample.txt", "w") as f:
    f.write("Hello, World!\nThis is a sample text file.\nPython file handling is powerful.")

# Reading an entire file at once
print("\nReading entire file:")
with open("sample.txt", "r") as file:
    contents = file.read()
    print(contents)

# Reading line by line
print("\nReading line by line:")
with open("sample.txt", "r") as file:
    for line in file:
        print(f"Line: {line.strip()}")  # strip() removes leading/trailing whitespace

# Reading all lines into a list
print("\nReading all lines into a list:")
with open("sample.txt", "r") as file:
    lines = file.readlines()
    print(f"Lines as list: {lines}")
    print(f"Number of lines: {len(lines)}")

# Reading specific lines
print("\nReading specific number of characters:")
with open("sample.txt", "r") as file:
    first_10_chars = file.read(10)
    print(f"First 10 characters: {first_10_chars}")

# =========== WRITING TO FILES ==========
print("\n===== WRITING TO FILES =====")

# 1. Writing to a text file
with open("output.txt", "w") as file:
    file.write("This is the first line.\n")
    file.write("This is the second line.\n")

print("Wrote to output.txt")

# 2. Appending to a text file
with open("output.txt", "a") as file:
    file.write("This line is appended.\n")
    file.write("And so is this one.\n")

print("Appended to output.txt")

# Reading the file we just created
with open("output.txt", "r") as file:
    print("\nContents of output.txt:")
    print(file.read())

# 3. Writing multiple lines at once
lines = ["Line 1", "Line 2", "Line 3", "Line 4"]
with open("multiple_lines.txt", "w") as file:
    file.writelines(f"{line}\n" for line in lines)

print("Wrote multiple lines to multiple_lines.txt")

# Reading the file we just created
with open("multiple_lines.txt", "r") as file:
    print("\nContents of multiple_lines.txt:")
    print(file.read())

# =========== FILE MODES ==========
print("\n===== FILE MODES =====")
print("'r'  - Read (default)")
print("'w'  - Write (creates new file or truncates existing file)")
print("'a'  - Append (creates new file or appends to existing file)")
print("'r+' - Read and write")
print("'b'  - Binary mode (e.g., 'rb' or 'wb')")
print("'t'  - Text mode (default)")

# =========== WORKING WITH PATHS ==========
print("\n===== WORKING WITH PATHS =====")
import os
import os.path

# Get current working directory
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# Join paths (works cross-platform)
file_path = os.path.join("data", "sample.txt")
print(f"Joined path: {file_path}")

# Check if file exists
sample_exists = os.path.exists("sample.txt")
print(f"sample.txt exists: {sample_exists}")

# Get file information
if sample_exists:
    size = os.path.getsize("sample.txt")
    modification_time = os.path.getmtime("sample.txt")
    print(f"File size: {size} bytes")
    print(f"Last modified: {modification_time}")

# =========== WORKING WITH DIRECTORIES ==========
print("\n===== WORKING WITH DIRECTORIES =====")

# Create a directory
if not os.path.exists("data"):
    os.mkdir("data")
    print("Created 'data' directory")

# List files in a directory
files = os.listdir(".")
print(f"Files in current directory: {files}")

# Create a file in the data directory
with open(os.path.join("data", "info.txt"), "w") as file:
    file.write("This file is in the data directory.")

print("Created file in data directory")

# =========== WORKING WITH CSV FILES ==========
print("\n===== WORKING WITH CSV FILES =====")
import csv

# Create a sample CSV file
with open("data.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age", "City"])  # Header row
    writer.writerow(["Alice", 30, "New York"])
    writer.writerow(["Bob", 25, "Los Angeles"])
    writer.writerow(["Charlie", 35, "Chicago"])

print("Created data.csv")

# Reading from a CSV file
with open("data.csv", "r", newline='') as file:
    reader = csv.reader(file)
    print("\nCSV Contents:")
    for row in reader:
        print(row)

# Using DictReader to read CSV as dictionaries
with open("data.csv", "r", newline='') as file:
    reader = csv.DictReader(file)
    print("\nCSV Contents as dictionaries:")
    for row in reader:
        print(row)

# =========== WORKING WITH JSON ==========
print("\n===== WORKING WITH JSON =====")
import json

# Create a Python dictionary
data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "languages": ["Python", "JavaScript", "Go"],
    "is_employee": True,
    "address": {
        "street": "123 Main St",
        "zip": "10001"
    }
}

# Write JSON to a file
with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

print("Wrote data to data.json")

# Read JSON from a file
with open("data.json", "r") as file:
    loaded_data = json.load(file)

print("\nLoaded JSON data:")
print(f"Name: {loaded_data['name']}")
print(f"Languages: {loaded_data['languages']}")
print(f"Address ZIP: {loaded_data['address']['zip']}")

# Convert Python object to JSON string
json_string = json.dumps(data, indent=2)
print("\nJSON string representation:")
print(json_string)

# =========== EXERCISES ==========
"""
Exercise 1: Create a program that reads a text file, counts the number of lines, 
            words, and characters, and prints the results.

Exercise 2: Write a program that takes a CSV file containing student records 
            (name, score1, score2, score3) and creates a new CSV file with each 
            student's name and average score.

Exercise 3: Create a function that reads a JSON file containing a list of products 
            (with properties like name, price, and quantity), finds the most expensive
            product, and prints its details.

Exercise 4: Write a program that recursively searches for files with a specific extension
            (e.g., .txt) in a directory and its subdirectories, and creates a list of
            all matching files with their full paths.

Exercise 5: Implement a simple note-taking app that allows the user to create, view,
            and delete notes, with each note stored as a separate text file.
"""