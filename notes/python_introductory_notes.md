# Elementary Python Programming Concepts

## Table of Contents

1. [Getting Started with Python](#getting-started-with-python)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Data Structures](#data-structures)
9. [String Manipulation](#string-manipulation)
10. [Error Handling](#error-handling)
11. [File Operations](#file-operations)
12. [Practice Exercises](#practice-exercises)

---

## Getting Started with Python

### What is Python?

Python is a high-level, interpreted programming language known for its:
- **Simple syntax**: Easy to read and write
- **Versatility**: Used in web development, data science, AI, automation
- **Large community**: Extensive libraries and support
- **Cross-platform**: Runs on Windows, Mac, Linux

### Your First Python Program

```python
# This is a comment - it doesn't run as code
print("Hello, World!")
```

**Output:**
```
Hello, World!
```

### Running Python Code

- **Interactive mode**: Type `python` in terminal
- **Script mode**: Save code in `.py` file and run with `python filename.py`
- **IDE/Editor**: Use tools like VS Code, PyCharm, or IDLE

---

## Variables and Data Types

### Variables

Variables are containers that store data values.

```python
# Creating variables
name = "Alice"
age = 25
height = 5.6
is_student = True

print(name)    # Alice
print(age)     # 25
print(height)  # 5.6
print(is_student)  # True
```

### Basic Data Types

#### 1. Integers (int)
```python
# Whole numbers
number = 42
negative = -10
large_number = 1000000

print(type(number))  # <class 'int'>
```

#### 2. Floating Point Numbers (float)
```python
# Decimal numbers
price = 19.99
temperature = -3.5
scientific = 1.5e6  # Scientific notation (1,500,000)

print(type(price))  # <class 'float'>
```

#### 3. Strings (str)
```python
# Text data
first_name = "John"
last_name = 'Doe'
message = """This is a
multi-line string"""

print(type(first_name))  # <class 'str'>
```

#### 4. Booleans (bool)
```python
# True or False values
is_sunny = True
is_raining = False
result = 5 > 3  # True

print(type(is_sunny))  # <class 'bool'>
```

### Variable Naming Rules

```python
# Valid variable names
user_name = "Alice"
age2 = 25
_private = "secret"
firstName = "John"  # camelCase
CONSTANT = 100

# Invalid variable names (these will cause errors)
# 2age = 25        # Can't start with number
# user-name = "Bob" # Can't use hyphens
# class = "Math"   # Can't use reserved keywords
```

---

## Basic Operations

### Arithmetic Operators

```python
a = 10
b = 3

# Basic arithmetic
addition = a + b        # 13
subtraction = a - b     # 7
multiplication = a * b  # 30
division = a / b        # 3.333...
floor_division = a // b # 3 (rounds down)
modulus = a % b         # 1 (remainder)
exponentiation = a ** b # 1000 (10^3)

print(f"10 + 3 = {addition}")
print(f"10 / 3 = {division}")
print(f"10 // 3 = {floor_division}")
print(f"10 % 3 = {modulus}")
```

### Comparison Operators

```python
x = 5
y = 10

# Comparison operations return True or False
equal = x == y          # False
not_equal = x != y      # True
less_than = x < y       # True
greater_than = x > y    # False
less_equal = x <= y     # True
greater_equal = x >= y  # False

print(f"5 == 10: {equal}")
print(f"5 < 10: {less_than}")
```

### Logical Operators

```python
# Logical operators: and, or, not
a = True
b = False

and_result = a and b    # False
or_result = a or b      # True
not_result = not a      # False

# Practical example
age = 20
has_license = True
can_drive = age >= 18 and has_license  # True

print(f"Can drive: {can_drive}")
```

---

## Input and Output

### Getting User Input

```python
# input() always returns a string
name = input("What's your name? ")
print(f"Hello, {name}!")

# Converting input to numbers
age_str = input("How old are you? ")
age = int(age_str)  # Convert string to integer

# Or do it in one line
height = float(input("What's your height in meters? "))

print(f"You are {age} years old and {height}m tall")
```

### Formatting Output

```python
name = "Alice"
age = 25
gpa = 3.85

# Different ways to format output
print("Hello", name)  # Simple comma separation
print("Name:", name, "Age:", age)

# String concatenation
print("Hello " + name)

# f-strings (recommended for Python 3.6+)
print(f"Hello {name}, you are {age} years old")
print(f"Your GPA is {gpa:.2f}")  # 2 decimal places

# .format() method
print("Hello {}, you are {} years old".format(name, age))
print("Your GPA is {:.2f}".format(gpa))

# % formatting (older style)
print("Hello %s, you are %d years old" % (name, age))
```

---

## Conditional Statements

### if, elif, else

```python
# Basic if statement
age = 18

if age >= 18:
    print("You are an adult")
    print("You can vote")

# if-else
temperature = 25

if temperature > 30:
    print("It's hot outside")
else:
    print("It's not too hot")

# if-elif-else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")
```

### Nested Conditions

```python
weather = "sunny"
temperature = 25

if weather == "sunny":
    if temperature > 20:
        print("Great day for a picnic!")
    else:
        print("Sunny but a bit cold")
else:
    print("Maybe stay inside")
```

### Multiple Conditions

```python
age = 20
has_id = True

# Using 'and'
if age >= 18 and has_id:
    print("You can enter the club")

# Using 'or'
day = "Saturday"
if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")

# Using 'in' for multiple values
fruit = "apple"
if fruit in ["apple", "banana", "orange"]:
    print("That's a common fruit")
```

---

## Loops

### for Loops

```python
# Loop through a range of numbers
print("Counting to 5:")
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

# Loop with start, stop, step
print("\nEven numbers from 2 to 10:")
for num in range(2, 11, 2):  # 2, 4, 6, 8, 10
    print(num)

# Loop through a string
word = "Python"
print(f"\nLetters in '{word}':")
for letter in word:
    print(letter)

# Loop through a list
fruits = ["apple", "banana", "cherry"]
print("\nFruits:")
for fruit in fruits:
    print(f"I like {fruit}")

# enumerate() for index and value
print("\nFruits with index:")
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

### while Loops

```python
# Basic while loop
count = 0
while count < 5:
    print(f"Count is: {count}")
    count += 1  # Same as count = count + 1

# User input validation
while True:
    password = input("Enter password: ")
    if password == "secret123":
        print("Access granted!")
        break  # Exit the loop
    else:
        print("Wrong password, try again")

# While with else
num = 1
while num <= 3:
    print(f"Number: {num}")
    num += 1
else:
    print("Loop completed normally")
```

### Loop Control

```python
# break: Exit loop immediately
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0, 1, 2, 3, 4

print()

# continue: Skip rest of current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)  # Prints 0, 1, 3, 4

print()

# Nested loops with break
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            break
        print(f"i={i}, j={j}")
```

---

## Functions

### Defining Functions

```python
# Basic function
def greet():
    print("Hello, World!")

# Call the function
greet()

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

# Function with multiple parameters
def add_numbers(a, b):
    result = a + b
    return result

sum_result = add_numbers(5, 3)
print(f"5 + 3 = {sum_result}")
```

### Function Parameters

```python
# Default parameters
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")                    # Hello, Alice!
greet("Bob", "Hi")               # Hi, Bob!
greet("Charlie", greeting="Hey") # Hey, Charlie!

# Multiple return values
def get_name_age():
    name = "Alice"
    age = 25
    return name, age

person_name, person_age = get_name_age()
print(f"Name: {person_name}, Age: {person_age}")

# Variable number of arguments
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15
```

### Scope

```python
# Global vs Local scope
global_var = "I'm global"

def my_function():
    local_var = "I'm local"
    print(global_var)  # Can access global
    print(local_var)   # Can access local

my_function()
print(global_var)  # Works
# print(local_var)  # Error! local_var not accessible here

# Modifying global variables
counter = 0

def increment():
    global counter
    counter += 1

print(f"Counter: {counter}")  # 0
increment()
print(f"Counter: {counter}")  # 1
```

---

## Data Structures

### Lists

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]
empty_list = []

# Accessing elements (0-indexed)
print(fruits[0])    # apple
print(fruits[-1])   # cherry (last element)
print(fruits[1:3])  # ['banana', 'cherry'] (slicing)

# Modifying lists
fruits.append("orange")          # Add to end
fruits.insert(1, "grape")        # Insert at position
fruits.remove("banana")          # Remove by value
popped = fruits.pop()            # Remove and return last
fruits[0] = "pineapple"         # Change by index

print(fruits)

# List methods
numbers = [3, 1, 4, 1, 5, 9, 2]
print(f"Length: {len(numbers)}")      # 7
print(f"Max: {max(numbers)}")         # 9
print(f"Min: {min(numbers)}")         # 1
print(f"Sum: {sum(numbers)}")         # 25
numbers.sort()                        # Sort in place
print(f"Sorted: {numbers}")
```

### Tuples

```python
# Tuples are immutable (can't be changed)
coordinates = (3, 5)
rgb_color = (255, 128, 0)
person = ("Alice", 25, "Engineer")

# Accessing tuple elements
print(coordinates[0])  # 3
print(person[1])       # 25

# Tuple unpacking
x, y = coordinates
name, age, job = person
print(f"Name: {name}, Age: {age}, Job: {job}")

# Tuples with one element need a comma
single_tuple = (42,)  # Note the comma
not_tuple = (42)      # This is just parentheses around a number
```

### Dictionaries

```python
# Creating dictionaries
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A",
    "courses": ["Math", "Science", "English"]
}

# Accessing values
print(student["name"])           # Alice
print(student.get("age"))        # 20
print(student.get("height", 0))  # 0 (default if key doesn't exist)

# Modifying dictionaries
student["age"] = 21              # Update existing
student["height"] = 5.6          # Add new key-value pair
del student["grade"]             # Remove key-value pair

# Dictionary methods
print(student.keys())            # All keys
print(student.values())          # All values
print(student.items())           # All key-value pairs

# Looping through dictionaries
for key in student:
    print(f"{key}: {student[key]}")

for key, value in student.items():
    print(f"{key}: {value}")
```

### Sets

```python
# Sets contain unique elements
fruits = {"apple", "banana", "cherry", "apple"}  # Duplicate removed
print(fruits)  # {'apple', 'banana', 'cherry'}

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1.union(set2))        # {1, 2, 3, 4, 5, 6}
print(set1.intersection(set2)) # {3, 4}
print(set1.difference(set2))   # {1, 2}

# Adding and removing
fruits.add("orange")
fruits.remove("banana")  # Error if not found
fruits.discard("grape")  # No error if not found
```

---

## String Manipulation

### String Basics

```python
text = "Hello, World!"

# String properties
print(len(text))      # 13
print(text.upper())   # HELLO, WORLD!
print(text.lower())   # hello, world!
print(text.title())   # Hello, World!

# String checking
print(text.startswith("Hello"))  # True
print(text.endswith("!"))        # True
print("World" in text)           # True
print(text.isdigit())           # False
print("123".isdigit())          # True
```

### String Methods

```python
sentence = "  The quick brown fox jumps  "

# Whitespace handling
print(sentence.strip())       # Remove leading/trailing whitespace
print(sentence.lstrip())      # Remove leading whitespace
print(sentence.rstrip())      # Remove trailing whitespace

# Splitting and joining
words = sentence.strip().split()  # Split into list of words
print(words)
rejoined = " ".join(words)        # Join list back to string
print(rejoined)

# Replacing
new_sentence = sentence.replace("fox", "cat")
print(new_sentence)

# Finding
position = sentence.find("quick")  # Returns index or -1
print(f"'quick' found at position: {position}")
```

### String Formatting

```python
name = "Alice"
age = 25
pi = 3.14159

# f-strings (Python 3.6+)
print(f"Name: {name}, Age: {age}")
print(f"Pi to 2 decimal places: {pi:.2f}")

# Format method
print("Name: {}, Age: {}".format(name, age))
print("Pi to 3 decimal places: {:.3f}".format(pi))

# Multiple lines
message = f"""
Dear {name},
You are {age} years old.
Best regards,
Python
"""
print(message)
```

---

## Error Handling

### Common Errors

```python
# Syntax Error - Code won't run
# print("Hello"  # Missing closing parenthesis

# Runtime Errors
try:
    number = int("abc")  # ValueError
except ValueError:
    print("That's not a valid number!")

try:
    result = 10 / 0  # ZeroDivisionError
except ZeroDivisionError:
    print("Cannot divide by zero!")

try:
    my_list = [1, 2, 3]
    print(my_list[5])  # IndexError
except IndexError:
    print("Index out of range!")
```

### try-except Blocks

```python
# Basic try-except
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None

print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # Error message, returns None

# Multiple exceptions
def get_integer():
    while True:
        try:
            value = int(input("Enter an integer: "))
            return value
        except ValueError:
            print("That's not a valid integer. Try again.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return None

# try-except-else-finally
def file_operations():
    try:
        # Code that might raise an exception
        file = open("data.txt", "r")
        content = file.read()
    except FileNotFoundError:
        print("File not found!")
        content = ""
    else:
        # Runs if no exception occurred
        print("File read successfully!")
    finally:
        # Always runs, regardless of exceptions
        if 'file' in locals():
            file.close()
    
    return content
```

---

## File Operations

### Reading Files

```python
# Reading entire file
try:
    with open("example.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("File not found!")

# Reading line by line
try:
    with open("example.txt", "r") as file:
        for line_number, line in enumerate(file, 1):
            print(f"Line {line_number}: {line.strip()}")
except FileNotFoundError:
    print("File not found!")

# Reading all lines into a list
try:
    with open("example.txt", "r") as file:
        lines = file.readlines()
        print(f"File has {len(lines)} lines")
except FileNotFoundError:
    print("File not found!")
```

### Writing Files

```python
# Writing to a file (overwrites existing content)
data = ["apple", "banana", "cherry"]

with open("fruits.txt", "w") as file:
    for fruit in data:
        file.write(fruit + "\n")

# Appending to a file
with open("fruits.txt", "a") as file:
    file.write("orange\n")
    file.write("grape\n")

# Writing multiple lines at once
lines = ["First line\n", "Second line\n", "Third line\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

### File Modes

```python
# Different file modes:
# "r" - Read (default)
# "w" - Write (overwrites)
# "a" - Append
# "x" - Create (fails if exists)
# "b" - Binary mode
# "t" - Text mode (default)

# Reading binary file
with open("image.jpg", "rb") as file:
    binary_data = file.read()

# Writing binary file
with open("copy.jpg", "wb") as file:
    file.write(binary_data)
```

---

## Practice Exercises

### Exercise 1: Calculator

```python
def calculator():
    """Simple calculator program"""
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("Enter first number: "))
            operation = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
            
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("Error: Division by zero!")
                    continue
            else:
                print("Invalid operation!")
                continue
            
            print(f"Result: {num1} {operation} {num2} = {result}")
            
            if input("Continue? (y/n): ").lower() != 'y':
                break
                
        except ValueError:
            print("Invalid input! Please enter numbers.")

# calculator()  # Uncomment to run
```

### Exercise 2: Word Counter

```python
def count_words(text):
    """Count frequency of words in text"""
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # Count word frequencies
    word_count = {}
    for word in words:
        # Remove punctuation
        clean_word = word.strip(".,!?;:")
        if clean_word:
            word_count[clean_word] = word_count.get(clean_word, 0) + 1
    
    return word_count

def display_word_stats(word_count):
    """Display word statistics"""
    print(f"Total unique words: {len(word_count)}")
    print(f"Total words: {sum(word_count.values())}")
    print("\nMost common words:")
    
    # Sort by count (descending)
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    for word, count in sorted_words[:5]:  # Top 5
        print(f"'{word}': {count}")

# Example usage
sample_text = """
Python is a great programming language. Python is easy to learn.
Many people love Python because Python is versatile and powerful.
"""

word_frequencies = count_words(sample_text)
display_word_stats(word_frequencies)
```

### Exercise 3: Number Guessing Game

```python
import random

def guessing_game():
    """Number guessing game"""
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: "))
            attempts += 1
            
            if guess == secret_number:
                print(f"Congratulations! You guessed it in {attempts} attempts!")
                break
            elif guess < secret_number:
                print("Too low!")
            else:
                print("Too high!")
                
            if attempts == max_attempts:
                print(f"Game over! The number was {secret_number}")
                
        except ValueError:
            print("Please enter a valid number!")
            
    play_again = input("Play again? (y/n): ").lower()
    if play_again == 'y':
        guessing_game()

# guessing_game()  # Uncomment to run
```

### Exercise 4: To-Do List Manager

```python
def todo_manager():
    """Simple to-do list manager"""
    todos = []
    
    while True:
        print("\n=== TO-DO LIST MANAGER ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task complete")
        print("4. Remove task")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            task = input("Enter new task: ")
            todos.append({"task": task, "completed": False})
            print("Task added!")
            
        elif choice == "2":
            if not todos:
                print("No tasks yet!")
            else:
                print("\nYour tasks:")
                for i, todo in enumerate(todos, 1):
                    status = "✓" if todo["completed"] else "○"
                    print(f"{i}. {status} {todo['task']}")
                    
        elif choice == "3":
            if not todos:
                print("No tasks to complete!")
            else:
                try:
                    task_num = int(input("Enter task number to complete: ")) - 1
                    if 0 <= task_num < len(todos):
                        todos[task_num]["completed"] = True
                        print("Task marked as complete!")
                    else:
                        print("Invalid task number!")
                except ValueError:
                    print("Please enter a valid number!")
                    
        elif choice == "4":
            if not todos:
                print("No tasks to remove!")
            else:
                try:
                    task_num = int(input("Enter task number to remove: ")) - 1
                    if 0 <= task_num < len(todos):
                        removed = todos.pop(task_num)
                        print(f"Removed: {removed['task']}")
                    else:
                        print("Invalid task number!")
                except ValueError:
                    print("Please enter a valid number!")
                    
        elif choice == "5":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")

# todo_manager()  # Uncomment to run
```

---

## Summary

These notes cover the fundamental concepts of Python programming:

1. **Variables and Data Types**: Store and work with different kinds of data
2. **Operations**: Perform calculations and comparisons
3. **Control Flow**: Make decisions and repeat actions with conditions and loops
4. **Functions**: Organize code into reusable blocks
5. **Data Structures**: Work with collections of data (lists, dictionaries, etc.)
6. **String Manipulation**: Process and format text
7. **Error Handling**: Deal with problems gracefully
8. **File Operations**: Read from and write to files

### Next Steps

1. Practice the exercises provided
2. Build small projects combining multiple concepts
3. Learn about modules and libraries
4. Explore object-oriented programming
5. Study algorithms and data structures
6. Work on real-world applications

### Additional Resources

- **Python Official Documentation**: https://docs.python.org/
- **Python Tutorial**: https://docs.python.org/tutorial/
- **Practice Problems**: HackerRank, LeetCode, Codewars
- **Books**: "Python Crash Course", "Automate the Boring Stuff with Python"

Remember: Programming is learned by doing. Practice regularly and build projects to reinforce these concepts!