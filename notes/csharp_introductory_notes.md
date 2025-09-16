# Elementary C# Programming Concepts

## Table of Contents

1. [Getting Started with C#](#getting-started-with-c)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Methods](#methods)
8. [Arrays and Collections](#arrays-and-collections)
9. [String Manipulation](#string-manipulation)
10. [Error Handling](#error-handling)
11. [File Operations](#file-operations)
12. [Classes and Objects](#classes-and-objects)
13. [Practice Exercises](#practice-exercises)

---

## Getting Started with C#

### What is C#?

C# (pronounced "C-Sharp") is a modern, object-oriented programming language developed by Microsoft. Key features:
- **Strongly typed**: Variables must be declared with specific types
- **Object-oriented**: Everything is based on classes and objects
- **Memory managed**: Automatic garbage collection
- **Cross-platform**: Runs on Windows, Mac, Linux with .NET
- **Versatile**: Used for web, desktop, mobile, and game development

### Your First C# Program

```csharp
using System;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            // This is a comment
            Console.WriteLine("Hello, World!");
            Console.ReadKey(); // Wait for key press
        }
    }
}
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **using System;** - Imports the System namespace for Console operations
- **namespace** - Organizes code into logical groups
- **class Program** - Defines a class (everything in C# is in a class)
- **static void Main** - Entry point of the program
- **Console.WriteLine()** - Prints text to console
- **Console.ReadKey()** - Waits for user input (keeps console open)

### Development Environment

- **Visual Studio**: Full-featured IDE (recommended for beginners)
- **Visual Studio Code**: Lightweight editor with C# extension
- **JetBrains Rider**: Professional IDE
- **.NET SDK**: Required to compile and run C# programs

---

## Variables and Data Types

### Variable Declaration

In C#, you must declare variables with their type before using them.

```csharp
using System;

class Program
{
    static void Main()
    {
        // Declaring variables
        string name = "Alice";
        int age = 25;
        double height = 5.6;
        bool isStudent = true;
        
        Console.WriteLine($"Name: {name}");
        Console.WriteLine($"Age: {age}");
        Console.WriteLine($"Height: {height}");
        Console.WriteLine($"Is Student: {isStudent}");
    }
}
```

### Basic Data Types

#### 1. Integer Types
```csharp
// Different integer types
byte smallNumber = 255;        // 0 to 255
short shortNumber = 32000;     // -32,768 to 32,767
int number = 2000000;          // -2.1 billion to 2.1 billion
long bigNumber = 9000000000L;  // Very large integers

Console.WriteLine($"int: {number}, type: {number.GetType()}");
```

#### 2. Floating Point Types
```csharp
// Decimal numbers
float precision = 3.14f;       // 7 digits precision
double price = 19.99;          // 15-17 digits precision  
decimal money = 1000.50m;      // 28-29 digits precision (for financial)

Console.WriteLine($"float: {precision}");
Console.WriteLine($"double: {price}");
Console.WriteLine($"decimal: {money}");
```

#### 3. Character and String Types
```csharp
// Characters and text
char grade = 'A';              // Single character
string firstName = "John";     // Text string
string lastName = "Doe";

Console.WriteLine($"Grade: {grade}");
Console.WriteLine($"Full name: {firstName} {lastName}");
```

#### 4. Boolean Type
```csharp
// True or false values
bool isRaining = false;
bool isSunny = true;
bool result = 5 > 3;           // true

Console.WriteLine($"Is raining: {isRaining}");
Console.WriteLine($"5 > 3: {result}");
```

### Variable Initialization

```csharp
// Different ways to declare and initialize
int a = 10;                    // Declaration with initialization
int b;                         // Declaration only
b = 20;                        // Assignment later

// Multiple variables of same type
int x = 1, y = 2, z = 3;

// Type inference with 'var' keyword
var name = "Alice";            // Compiler infers string
var count = 42;                // Compiler infers int
var price = 19.99;             // Compiler infers double

// Constants (cannot be changed)
const double PI = 3.14159;
const string COMPANY_NAME = "TechCorp";
```

### Variable Naming Rules

```csharp
// Valid variable names (camelCase convention)
int age = 25;
string firstName = "John";
double accountBalance = 1000.50;
bool isUserLoggedIn = true;

// Valid but not conventional
int _privateVar = 10;
int number2 = 20;

// Invalid variable names (these cause compilation errors)
// int 2age = 25;        // Can't start with number
// int user-name = "Bob"; // Can't use hyphens
// int class = "Math";   // Can't use reserved keywords
```

---

## Basic Operations

### Arithmetic Operators

```csharp
using System;

class Program
{
    static void Main()
    {
        int a = 10;
        int b = 3;
        
        // Basic arithmetic
        int addition = a + b;           // 13
        int subtraction = a - b;        // 7
        int multiplication = a * b;     // 30
        double division = (double)a / b; // 3.333... (cast to double)
        int integerDivision = a / b;    // 3 (integer division)
        int modulus = a % b;            // 1 (remainder)
        
        Console.WriteLine($"10 + 3 = {addition}");
        Console.WriteLine($"10 / 3 = {division:F2}"); // Format to 2 decimal places
        Console.WriteLine($"10 % 3 = {modulus}");
        
        // Compound assignment operators
        int x = 5;
        x += 3;  // x = x + 3, now x = 8
        x -= 2;  // x = x - 2, now x = 6
        x *= 2;  // x = x * 2, now x = 12
        x /= 4;  // x = x / 4, now x = 3
        
        Console.WriteLine($"Final x value: {x}");
        
        // Increment and decrement
        int counter = 5;
        counter++;    // Post-increment, counter = 6
        ++counter;    // Pre-increment, counter = 7
        counter--;    // Post-decrement, counter = 6
        --counter;    // Pre-decrement, counter = 5
        
        Console.WriteLine($"Counter: {counter}");
    }
}
```

### Comparison Operators

```csharp
using System;

class Program
{
    static void Main()
    {
        int x = 5;
        int y = 10;
        
        // Comparison operations return bool
        bool equal = x == y;          // false
        bool notEqual = x != y;       // true
        bool lessThan = x < y;        // true
        bool greaterThan = x > y;     // false
        bool lessEqual = x <= y;      // true
        bool greaterEqual = x >= y;   // false
        
        Console.WriteLine($"5 == 10: {equal}");
        Console.WriteLine($"5 < 10: {lessThan}");
        Console.WriteLine($"5 != 10: {notEqual}");
    }
}
```

### Logical Operators

```csharp
using System;

class Program
{
    static void Main()
    {
        // Logical operators: &&, ||, !
        bool a = true;
        bool b = false;
        
        bool andResult = a && b;    // false (both must be true)
        bool orResult = a || b;     // true (at least one must be true)
        bool notResult = !a;        // false (opposite of a)
        
        Console.WriteLine($"true && false = {andResult}");
        Console.WriteLine($"true || false = {orResult}");
        Console.WriteLine($"!true = {notResult}");
        
        // Practical example
        int age = 20;
        bool hasLicense = true;
        bool canDrive = age >= 18 && hasLicense;
        
        Console.WriteLine($"Can drive: {canDrive}");
    }
}
```

---

## Input and Output

### Getting User Input

```csharp
using System;

class Program
{
    static void Main()
    {
        // Reading string input
        Console.Write("What's your name? ");
        string name = Console.ReadLine();
        Console.WriteLine($"Hello, {name}!");
        
        // Reading and converting numeric input
        Console.Write("How old are you? ");
        string ageInput = Console.ReadLine();
        int age = int.Parse(ageInput);
        
        // Alternative: TryParse (safer)
        Console.Write("What's your height in meters? ");
        string heightInput = Console.ReadLine();
        
        if (double.TryParse(heightInput, out double height))
        {
            Console.WriteLine($"You are {age} years old and {height}m tall");
        }
        else
        {
            Console.WriteLine("Invalid height entered");
        }
        
        // Reading single character
        Console.Write("Press any key to continue...");
        ConsoleKeyInfo keyInfo = Console.ReadKey();
        Console.WriteLine($"\nYou pressed: {keyInfo.Key}");
    }
}
```

### Formatting Output

```csharp
using System;

class Program
{
    static void Main()
    {
        string name = "Alice";
        int age = 25;
        double gpa = 3.85;
        
        // Different ways to format output
        Console.WriteLine("Hello " + name);  // String concatenation
        
        // String interpolation (recommended)
        Console.WriteLine($"Hello {name}, you are {age} years old");
        Console.WriteLine($"Your GPA is {gpa:F2}");  // 2 decimal places
        
        // Composite formatting
        Console.WriteLine("Hello {0}, you are {1} years old", name, age);
        Console.WriteLine("Your GPA is {0:F2}", gpa);
        
        // Format specifiers
        double money = 1234.56;
        DateTime now = DateTime.Now;
        
        Console.WriteLine($"Currency: {money:C}");        // $1,234.56
        Console.WriteLine($"Percentage: {0.85:P}");       // 85.00%
        Console.WriteLine($"Date: {now:yyyy-MM-dd}");     // 2024-01-15
        Console.WriteLine($"Time: {now:HH:mm:ss}");       // 14:30:25
    }
}
```

---

## Conditional Statements

### if, else if, else

```csharp
using System;

class Program
{
    static void Main()
    {
        // Basic if statement
        int age = 18;
        
        if (age >= 18)
        {
            Console.WriteLine("You are an adult");
            Console.WriteLine("You can vote");
        }
        
        // if-else
        int temperature = 25;
        
        if (temperature > 30)
        {
            Console.WriteLine("It's hot outside");
        }
        else
        {
            Console.WriteLine("It's not too hot");
        }
        
        // if-else if-else
        int score = 85;
        string grade;
        
        if (score >= 90)
        {
            grade = "A";
        }
        else if (score >= 80)
        {
            grade = "B";
        }
        else if (score >= 70)
        {
            grade = "C";
        }
        else if (score >= 60)
        {
            grade = "D";
        }
        else
        {
            grade = "F";
        }
        
        Console.WriteLine($"Your grade is: {grade}");
    }
}
```

### switch Statements

```csharp
using System;

class Program
{
    static void Main()
    {
        // Traditional switch statement
        Console.Write("Enter a day number (1-7): ");
        if (int.TryParse(Console.ReadLine(), out int dayNumber))
        {
            string dayName;
            
            switch (dayNumber)
            {
                case 1:
                    dayName = "Monday";
                    break;
                case 2:
                    dayName = "Tuesday";
                    break;
                case 3:
                    dayName = "Wednesday";
                    break;
                case 4:
                    dayName = "Thursday";
                    break;
                case 5:
                    dayName = "Friday";
                    break;
                case 6:
                    dayName = "Saturday";
                    break;
                case 7:
                    dayName = "Sunday";
                    break;
                default:
                    dayName = "Invalid day";
                    break;
            }
            
            Console.WriteLine($"Day {dayNumber} is {dayName}");
        }
        
        // Switch expression (C# 8.0+)
        string GetSeason(int month) => month switch
        {
            12 or 1 or 2 => "Winter",
            3 or 4 or 5 => "Spring",
            6 or 7 or 8 => "Summer",
            9 or 10 or 11 => "Fall",
            _ => "Invalid month"
        };
        
        Console.WriteLine($"Month 6 is in {GetSeason(6)}");
    }
}
```

### Ternary Operator

```csharp
using System;

class Program
{
    static void Main()
    {
        int age = 20;
        
        // Ternary operator: condition ? value_if_true : value_if_false
        string status = age >= 18 ? "Adult" : "Minor";
        Console.WriteLine($"Status: {status}");
        
        // Nested ternary (use sparingly)
        int score = 85;
        string grade = score >= 90 ? "A" : score >= 80 ? "B" : "C or below";
        Console.WriteLine($"Grade: {grade}");
        
        // Practical example
        int x = 10, y = 20;
        int max = x > y ? x : y;
        Console.WriteLine($"Maximum of {x} and {y} is {max}");
    }
}
```

---

## Loops

### for Loops

```csharp
using System;

class Program
{
    static void Main()
    {
        // Basic for loop
        Console.WriteLine("Counting to 5:");
        for (int i = 1; i <= 5; i++)
        {
            Console.WriteLine($"Count: {i}");
        }
        
        // Loop with different increment
        Console.WriteLine("\nEven numbers from 2 to 10:");
        for (int i = 2; i <= 10; i += 2)
        {
            Console.WriteLine(i);
        }
        
        // Counting backwards
        Console.WriteLine("\nCountdown:");
        for (int i = 5; i >= 1; i--)
        {
            Console.WriteLine(i);
        }
        Console.WriteLine("Blast off!");
        
        // Loop through array
        string[] fruits = {"apple", "banana", "cherry"};
        Console.WriteLine("\nFruits:");
        for (int i = 0; i < fruits.Length; i++)
        {
            Console.WriteLine($"{i + 1}. {fruits[i]}");
        }
    }
}
```

### foreach Loops

```csharp
using System;

class Program
{
    static void Main()
    {
        // foreach loop for arrays
        string[] colors = {"red", "green", "blue", "yellow"};
        
        Console.WriteLine("Colors:");
        foreach (string color in colors)
        {
            Console.WriteLine($"- {color}");
        }
        
        // foreach with different data types
        int[] numbers = {1, 2, 3, 4, 5};
        int sum = 0;
        
        foreach (int number in numbers)
        {
            sum += number;
        }
        
        Console.WriteLine($"Sum of numbers: {sum}");
        
        // foreach with string (each character)
        string word = "Hello";
        Console.WriteLine($"Letters in '{word}':");
        foreach (char letter in word)
        {
            Console.WriteLine(letter);
        }
    }
}
```

### while and do-while Loops

```csharp
using System;

class Program
{
    static void Main()
    {
        // Basic while loop
        int count = 0;
        while (count < 3)
        {
            Console.WriteLine($"Count is: {count}");
            count++;
        }
        
        // Input validation with while
        int number;
        while (true)
        {
            Console.Write("Enter a number between 1 and 10: ");
            if (int.TryParse(Console.ReadLine(), out number) && number >= 1 && number <= 10)
            {
                Console.WriteLine($"Valid number: {number}");
                break; // Exit the loop
            }
            else
            {
                Console.WriteLine("Invalid input. Try again.");
            }
        }
        
        // do-while loop (executes at least once)
        string input;
        do
        {
            Console.Write("Enter 'quit' to exit: ");
            input = Console.ReadLine();
            Console.WriteLine($"You entered: {input}");
        }
        while (input?.ToLower() != "quit");
        
        Console.WriteLine("Goodbye!");
    }
}
```

### Loop Control

```csharp
using System;

class Program
{
    static void Main()
    {
        // break: Exit loop immediately
        Console.WriteLine("Numbers with break:");
        for (int i = 0; i < 10; i++)
        {
            if (i == 5)
                break;
            Console.WriteLine(i); // Prints 0, 1, 2, 3, 4
        }
        
        // continue: Skip rest of current iteration
        Console.WriteLine("\nNumbers with continue (skip 3):");
        for (int i = 0; i < 6; i++)
        {
            if (i == 3)
                continue;
            Console.WriteLine(i); // Prints 0, 1, 2, 4, 5
        }
        
        // Nested loops with labeled break
        Console.WriteLine("\nNested loops:");
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                if (i == 1 && j == 1)
                    break; // Only breaks inner loop
                Console.WriteLine($"i={i}, j={j}");
            }
        }
    }
}
```

---

## Methods

### Defining Methods

```csharp
using System;

class Program
{
    // Method with no parameters and no return value
    static void SayHello()
    {
        Console.WriteLine("Hello from a method!");
    }
    
    // Method with parameters
    static void GreetPerson(string name)
    {
        Console.WriteLine($"Hello, {name}!");
    }
    
    // Method with return value
    static int AddNumbers(int a, int b)
    {
        int result = a + b;
        return result;
    }
    
    // Method with multiple parameters and return value
    static double CalculateArea(double length, double width)
    {
        return length * width;
    }
    
    static void Main()
    {
        // Calling methods
        SayHello();
        
        GreetPerson("Alice");
        GreetPerson("Bob");
        
        int sum = AddNumbers(5, 3);
        Console.WriteLine($"5 + 3 = {sum}");
        
        double area = CalculateArea(4.5, 6.2);
        Console.WriteLine($"Area: {area:F2}");
    }
}
```

### Method Overloading

```csharp
using System;

class Program
{
    // Method overloading - same name, different parameters
    static int Add(int a, int b)
    {
        return a + b;
    }
    
    static double Add(double a, double b)
    {
        return a + b;
    }
    
    static int Add(int a, int b, int c)
    {
        return a + b + c;
    }
    
    static string Add(string a, string b)
    {
        return a + b;
    }
    
    static void Main()
    {
        Console.WriteLine(Add(5, 3));           // Calls int version
        Console.WriteLine(Add(5.5, 3.2));      // Calls double version
        Console.WriteLine(Add(1, 2, 3));       // Calls three-parameter version
        Console.WriteLine(Add("Hello", " World")); // Calls string version
    }
}
```

### Parameters and Arguments

```csharp
using System;

class Program
{
    // Default parameters
    static void Greet(string name, string greeting = "Hello")
    {
        Console.WriteLine($"{greeting}, {name}!");
    }
    
    // ref parameter (pass by reference)
    static void DoubleValue(ref int number)
    {
        number *= 2;
    }
    
    // out parameter (must be assigned in method)
    static void GetNameAndAge(out string name, out int age)
    {
        name = "John Doe";
        age = 30;
    }
    
    // params keyword (variable number of arguments)
    static int SumAll(params int[] numbers)
    {
        int total = 0;
        foreach (int num in numbers)
        {
            total += num;
        }
        return total;
    }
    
    static void Main()
    {
        // Default parameters
        Greet("Alice");              // Uses default greeting
        Greet("Bob", "Hi");         // Uses custom greeting
        
        // ref parameter
        int value = 5;
        Console.WriteLine($"Before: {value}");
        DoubleValue(ref value);
        Console.WriteLine($"After: {value}");  // 10
        
        // out parameters
        GetNameAndAge(out string personName, out int personAge);
        Console.WriteLine($"Name: {personName}, Age: {personAge}");
        
        // params
        Console.WriteLine($"Sum: {SumAll(1, 2, 3)}");        // 6
        Console.WriteLine($"Sum: {SumAll(1, 2, 3, 4, 5)}");  // 15
    }
}
```

---

## Arrays and Collections

### Arrays

```csharp
using System;

class Program
{
    static void Main()
    {
        // Declaring and initializing arrays
        int[] numbers = new int[5];           // Array of 5 integers
        string[] fruits = {"apple", "banana", "cherry"}; // Initialize with values
        
        // Accessing array elements (0-indexed)
        numbers[0] = 10;
        numbers[1] = 20;
        numbers[2] = 30;
        
        Console.WriteLine($"First fruit: {fruits[0]}");
        Console.WriteLine($"Array length: {fruits.Length}");
        
        // Looping through arrays
        Console.WriteLine("Numbers:");
        for (int i = 0; i < numbers.Length; i++)
        {
            Console.WriteLine($"numbers[{i}] = {numbers[i]}");
        }
        
        Console.WriteLine("Fruits:");
        foreach (string fruit in fruits)
        {
            Console.WriteLine($"- {fruit}");
        }
        
        // Multi-dimensional arrays
        int[,] matrix = new int[2, 3] { {1, 2, 3}, {4, 5, 6} };
        
        Console.WriteLine("Matrix:");
        for (int row = 0; row < matrix.GetLength(0); row++)
        {
            for (int col = 0; col < matrix.GetLength(1); col++)
            {
                Console.Write($"{matrix[row, col]} ");
            }
            Console.WriteLine();
        }
        
        // Jagged arrays (array of arrays)
        int[][] jaggedArray = new int[3][];
        jaggedArray[0] = new int[4] {1, 2, 3, 4};
        jaggedArray[1] = new int[2] {5, 6};
        jaggedArray[2] = new int[3] {7, 8, 9};
        
        Console.WriteLine("Jagged array:");
        for (int i = 0; i < jaggedArray.Length; i++)
        {
            Console.Write($"Row {i}: ");
            for (int j = 0; j < jaggedArray[i].Length; j++)
            {
                Console.Write($"{jaggedArray[i][j]} ");
            }
            Console.WriteLine();
        }
    }
}
```

### Lists

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        // Creating lists (dynamic arrays)
        List<string> names = new List<string>();
        List<int> numbers = new List<int> {1, 2, 3, 4, 5};
        
        // Adding elements
        names.Add("Alice");
        names.Add("Bob");
        names.Add("Charlie");
        
        // Inserting at specific position
        names.Insert(1, "David");  // Insert at index 1
        
        // Accessing elements
        Console.WriteLine($"First name: {names[0]}");
        Console.WriteLine($"List count: {names.Count}");
        
        // Removing elements
        names.Remove("Bob");           // Remove by value
        names.RemoveAt(0);            // Remove by index
        
        // Checking if element exists
        if (names.Contains("Alice"))
        {
            Console.WriteLine("Alice is in the list");
        }
        
        // Looping through list
        Console.WriteLine("Names in list:");
        foreach (string name in names)
        {
            Console.WriteLine($"- {name}");
        }
        
        // List methods
        numbers.Sort();                    // Sort in ascending order
        numbers.Reverse();                 // Reverse the order
        
        Console.WriteLine("Sorted numbers (descending):");
        foreach (int num in numbers)
        {
            Console.Write($"{num} ");
        }
        Console.WriteLine();
        
        // Finding elements
        int index = numbers.IndexOf(3);
        Console.WriteLine($"Index of 3: {index}");
        
        // Converting to array
        string[] nameArray = names.ToArray();
        Console.WriteLine($"Converted to array, length: {nameArray.Length}");
    }
}
```

### Dictionaries

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        // Creating dictionaries (key-value pairs)
        Dictionary<string, int> ages = new Dictionary<string, int>();
        Dictionary<string, string> capitals = new Dictionary<string, string>
        {
            {"USA", "Washington D.C."},
            {"France", "Paris"},
            {"Japan", "Tokyo"}
        };
        
        // Adding key-value pairs
        ages["Alice"] = 25;
        ages["Bob"] = 30;
        ages.Add("Charlie", 35);
        
        // Accessing values
        Console.WriteLine($"Alice's age: {ages["Alice"]}");
        Console.WriteLine($"Capital of France: {capitals["France"]}");
        
        // Checking if key exists
        if (ages.ContainsKey("Bob"))
        {
            Console.WriteLine($"Bob's age: {ages["Bob"]}");
        }
        
        // Safe access with TryGetValue
        if (ages.TryGetValue("David", out int davidAge))
        {
            Console.WriteLine($"David's age: {davidAge}");
        }
        else
        {
            Console.WriteLine("David not found in dictionary");
        }
        
        // Modifying values
        ages["Alice"] = 26;  // Update existing
        
        // Removing key-value pairs
        ages.Remove("Charlie");
        
        // Looping through dictionary
        Console.WriteLine("\nAll ages:");
        foreach (KeyValuePair<string, int> pair in ages)
        {
            Console.WriteLine($"{pair.Key}: {pair.Value}");
        }
        
        // Alternative loop syntax
        Console.WriteLine("\nAll capitals:");
        foreach (var kvp in capitals)
        {
            Console.WriteLine($"{kvp.Key} -> {kvp.Value}");
        }
        
        // Getting all keys or values
        Console.WriteLine($"\nKeys: {string.Join(", ", ages.Keys)}");
        Console.WriteLine($"Values: {string.Join(", ", ages.Values)}");
    }
}
```

---

## String Manipulation

### String Basics

```csharp
using System;

class Program
{
    static void Main()
    {
        string text = "Hello, World!";
        
        // String properties and methods
        Console.WriteLine($"Length: {text.Length}");
        Console.WriteLine($"Uppercase: {text.ToUpper()}");
        Console.WriteLine($"Lowercase: {text.ToLower()}");
        
        // String checking methods
        Console.WriteLine($"Starts with 'Hello': {text.StartsWith("Hello")}");
        Console.WriteLine($"Ends with '!': {text.EndsWith("!")}");
        Console.WriteLine($"Contains 'World': {text.Contains("World")}");
        Console.WriteLine($"Is null or empty: {string.IsNullOrEmpty(text)}");
        Console.WriteLine($"Is null or whitespace: {string.IsNullOrWhiteSpace(text)}");
        
        // String indexing (strings are arrays of characters)
        Console.WriteLine($"First character: {text[0]}");
        Console.WriteLine($"Last character: {text[text.Length - 1]}");
        
        // Finding substrings
        int index = text.IndexOf("World");
        Console.WriteLine($"'World' found at index: {index}");
        
        int lastIndex = text.LastIndexOf("l");
        Console.WriteLine($"Last 'l' at index: {lastIndex}");
    }
}
```

### String Manipulation

```csharp
using System;

class Program
{
    static void Main()
    {
        string sentence = "  The quick brown fox jumps over the lazy dog  ";
        
        // Trimming whitespace
        Console.WriteLine($"Original: '{sentence}'");
        Console.WriteLine($"Trimmed: '{sentence.Trim()}'");
        Console.WriteLine($"Trim start