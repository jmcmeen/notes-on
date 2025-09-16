# Introductory C++ Programming Concepts

## Table of Contents

1. [Getting Started with C++](#getting-started-with-c)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Arrays and Vectors](#arrays-and-vectors)
9. [Pointers and References](#pointers-and-references)
10. [Classes and Objects](#classes-and-objects)
11. [String Manipulation](#string-manipulation)
12. [File Operations](#file-operations)
13. [Memory Management](#memory-management)
14. [Practice Exercises](#practice-exercises)

---

## Getting Started with C++

### What is C++?

C++ is a general-purpose programming language that extends C with object-oriented features. Key characteristics:
- **Compiled language**: Source code is translated to machine code
- **Statically typed**: Variable types are checked at compile time
- **Multi-paradigm**: Supports procedural, object-oriented, and generic programming
- **Performance-oriented**: Direct memory management and efficient execution
- **Standard Library**: Rich collection of data structures and algorithms

### Your First C++ Program

```cpp
#include <iostream>
using namespace std;

int main() {
    // This is a comment
    cout << "Hello, World!" << endl;
    return 0;
}
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **#include <iostream>** - Preprocessor directive to include input/output stream library
- **using namespace std** - Allows use of standard library names without std:: prefix
- **int main()** - Entry point of the program, returns an integer
- **cout** - Output stream object for printing to console
- **<<** - Stream insertion operator
- **endl** - End line manipulator (newline + flush)
- **return 0** - Indicates successful program termination

### Compilation Process

```bash
# Compile C++ source file
g++ -o program program.cpp

# Run the compiled program
./program
```

### Development Environment Options

- **Visual Studio**: Microsoft's IDE (Windows)
- **Code::Blocks**: Cross-platform IDE
- **CLion**: JetBrains IDE
- **VS Code**: Lightweight editor with C++ extensions
- **Command line**: g++, clang++, or MSVC compiler

---

## Variables and Data Types

### Variable Declaration and Initialization

```cpp
#include <iostream>
using namespace std;

int main() {
    // Declaration with initialization
    int age = 25;
    double height = 5.9;
    char grade = 'A';
    bool isStudent = true;
    
    // Declaration without initialization
    int count;
    count = 10;
    
    // Multiple declarations
    int x = 1, y = 2, z = 3;
    
    cout << "Age: " << age << endl;
    cout << "Height: " << height << endl;
    cout << "Grade: " << grade << endl;
    cout << "Is Student: " << isStudent << endl;
    
    return 0;
}
```

### Fundamental Data Types

#### Integer Types
```cpp
#include <iostream>
#include <climits>
using namespace std;

int main() {
    // Integer types with different sizes
    short shortVar = 32000;           // Usually 16 bits
    int intVar = 2000000000;          // Usually 32 bits
    long longVar = 3000000000L;       // Usually 32 or 64 bits
    long long llVar = 9000000000LL;   // At least 64 bits
    
    // Unsigned variants (only positive values)
    unsigned int positiveOnly = 4000000000U;
    
    // Display sizes and ranges
    cout << "Size of int: " << sizeof(int) << " bytes" << endl;
    cout << "Int range: " << INT_MIN << " to " << INT_MAX << endl;
    
    return 0;
}
```

#### Floating Point Types
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    float price = 19.99f;          // Single precision (32 bits)
    double distance = 384400.0;    // Double precision (64 bits)
    long double precise = 3.14159265358979323846L; // Extended precision
    
    // Scientific notation
    double sciNumber = 1.5e6;      // 1,500,000
    
    cout << fixed << setprecision(2);
    cout << "Price: $" << price << endl;
    cout << "Distance: " << distance << " km" << endl;
    
    cout << setprecision(10);
    cout << "Pi (long double): " << precise << endl;
    
    return 0;
}
```

#### Character Types
```cpp
#include <iostream>
using namespace std;

int main() {
    char letter = 'A';             // Single character
    char digit = '7';              // Character representation of digit
    char newline = '\n';           // Escape sequence
    
    // ASCII values
    cout << "Letter: " << letter << " (ASCII: " << (int)letter << ")" << endl;
    cout << "Digit: " << digit << " (ASCII: " << (int)digit << ")" << endl;
    
    // Common escape sequences
    cout << "Tab:\tTabbed text" << endl;
    cout << "Quote: \"Hello\"" << endl;
    cout << "Backslash: \\" << endl;
    
    return 0;
}
```

#### Boolean Type
```cpp
#include <iostream>
using namespace std;

int main() {
    bool isTrue = true;
    bool isFalse = false;
    bool result = (5 > 3);         // Comparison result
    
    // Display as text instead of 0/1
    cout << boolalpha;
    cout << "True: " << isTrue << endl;
    cout << "False: " << isFalse << endl;
    cout << "5 > 3: " << result << endl;
    
    return 0;
}
```

### Constants

```cpp
#include <iostream>
using namespace std;

int main() {
    // const keyword
    const double PI = 3.14159;
    const int MAX_SIZE = 100;
    
    // #define preprocessor directive (legacy style)
    #define SPEED_OF_LIGHT 299792458
    
    cout << "Pi: " << PI << endl;
    cout << "Max size: " << MAX_SIZE << endl;
    cout << "Speed of light: " << SPEED_OF_LIGHT << " m/s" << endl;
    
    // PI = 3.14; // Error: cannot modify const variable
    
    return 0;
}
```

### Type Conversion

```cpp
#include <iostream>
using namespace std;

int main() {
    // Implicit conversion (automatic)
    int intValue = 10;
    double doubleValue = intValue;    // int to double
    
    // Explicit conversion (casting)
    double pi = 3.14159;
    int truncatedPi = (int)pi;        // C-style cast
    int roundedPi = static_cast<int>(pi); // C++ style cast
    
    cout << "Original double: " << pi << endl;
    cout << "Truncated to int: " << truncatedPi << endl;
    
    // Character and integer conversion
    char letter = 'A';
    int asciiValue = letter;          // Implicit conversion
    char fromAscii = 66;              // ASCII 66 = 'B'
    
    cout << "Letter: " << letter << " ASCII: " << asciiValue << endl;
    cout << "ASCII 66: " << fromAscii << endl;
    
    return 0;
}
```

---

## Basic Operations

### Arithmetic Operators

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int a = 15;
    int b = 4;
    
    // Basic arithmetic
    cout << "a = " << a << ", b = " << b << endl;
    cout << "Addition: " << a + b << endl;        // 19
    cout << "Subtraction: " << a - b << endl;     // 11
    cout << "Multiplication: " << a * b << endl;  // 60
    cout << "Division: " << a / b << endl;        // 3 (integer division)
    cout << "Modulus: " << a % b << endl;         // 3 (remainder)
    
    // Floating point division
    double result = (double)a / b;
    cout << "Float division: " << result << endl; // 3.75
    
    // Power operation (requires cmath)
    double power = pow(a, 2);
    cout << "15^2 = " << power << endl;
    
    // Increment and decrement
    int counter = 5;
    cout << "Initial counter: " << counter << endl;
    cout << "Post-increment: " << counter++ << endl; // Prints 5, then increments
    cout << "Counter now: " << counter << endl;      // 6
    cout << "Pre-increment: " << ++counter << endl;  // Increments first, then prints 7
    
    return 0;
}
```

### Assignment Operators

```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 10;
    
    cout << "Initial x: " << x << endl;
    
    // Compound assignment operators
    x += 5;    // x = x + 5
    cout << "After x += 5: " << x << endl;        // 15
    
    x -= 3;    // x = x - 3
    cout << "After x -= 3: " << x << endl;        // 12
    
    x *= 2;    // x = x * 2
    cout << "After x *= 2: " << x << endl;        // 24
    
    x /= 4;    // x = x / 4
    cout << "After x /= 4: " << x << endl;        // 6
    
    x %= 4;    // x = x % 4
    cout << "After x %= 4: " << x << endl;        // 2
    
    return 0;
}
```

### Comparison Operators

```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 10;
    int y = 20;
    
    cout << "x = " << x << ", y = " << y << endl;
    cout << boolalpha; // Display bool as true/false
    
    cout << "x == y: " << (x == y) << endl;  // false
    cout << "x != y: " << (x != y) << endl;  // true
    cout << "x < y: " << (x < y) << endl;    // true
    cout << "x > y: " << (x > y) << endl;    // false
    cout << "x <= y: " << (x <= y) << endl;  // true
    cout << "x >= y: " << (x >= y) << endl;  // false
    
    return 0;
}
```

### Logical Operators

```cpp
#include <iostream>
using namespace std;

int main() {
    bool a = true;
    bool b = false;
    
    cout << boolalpha;
    cout << "a = " << a << ", b = " << b << endl;
    
    // Logical AND (&&)
    cout << "a && b: " << (a && b) << endl;  // false
    
    // Logical OR (||)
    cout << "a || b: " << (a || b) << endl;  // true
    
    // Logical NOT (!)
    cout << "!a: " << (!a) << endl;          // false
    cout << "!b: " << (!b) << endl;          // true
    
    // Practical example
    int age = 20;
    bool hasLicense = true;
    bool canDrive = (age >= 16) && hasLicense;
    
    cout << "Can drive: " << canDrive << endl;
    
    // Short-circuit evaluation
    int num = 0;
    if (num != 0 && 10 / num > 1) {
        cout << "This won't execute" << endl;
    }
    
    return 0;
}
```

---

## Input and Output

### Basic Input/Output

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int age;
    double height;
    
    // Getting input
    cout << "Enter your name: ";
    getline(cin, name);              // Read entire line including spaces
    
    cout << "Enter your age: ";
    cin >> age;
    
    cout << "Enter your height (in meters): ";
    cin >> height;
    
    // Displaying output
    cout << "\nHello, " << name << "!" << endl;
    cout << "You are " << age << " years old." << endl;
    cout << "Your height is " << height << " meters." << endl;
    
    return 0;
}
```

### Input Validation

```cpp
#include <iostream>
#include <limits>
using namespace std;

int main() {
    int number;
    
    cout << "Enter an integer: ";
    
    // Input validation loop
    while (!(cin >> number)) {
        cout << "Invalid input. Please enter a valid integer: ";
        cin.clear();                    // Clear error flags
        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Ignore invalid input
    }
    
    cout << "You entered: " << number << endl;
    
    return 0;
}
```

### Formatted Output

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double pi = 3.14159265359;
    int number = 42;
    
    // Set precision
    cout << "Default: " << pi << endl;
    cout << fixed << setprecision(2) << "2 decimal places: " << pi << endl;
    cout << setprecision(4) << "4 decimal places: " << pi << endl;
    
    // Field width and alignment
    cout << "\nFormatted table:" << endl;
    cout << setw(10) << "Number" << setw(15) << "Square" << endl;
    cout << setfill('-') << setw(25) << "" << setfill(' ') << endl;
    
    for (int i = 1; i <= 5; i++) {
        cout << setw(10) << i << setw(15) << i * i << endl;
    }
    
    // Different number bases
    cout << "\nNumber " << number << " in different bases:" << endl;
    cout << "Decimal: " << dec << number << endl;
    cout << "Hexadecimal: " << hex << number << endl;
    cout << "Octal: " << oct << number << endl;
    
    return 0;
}
```

---

## Conditional Statements

### if, else if, else

```cpp
#include <iostream>
using namespace std;

int main() {
    int score;
    
    cout << "Enter your test score (0-100): ";
    cin >> score;
    
    // Nested if-else statements
    if (score >= 90) {
        cout << "Grade: A - Excellent!" << endl;
    }
    else if (score >= 80) {
        cout << "Grade: B - Good job!" << endl;
    }
    else if (score >= 70) {
        cout << "Grade: C - Satisfactory" << endl;
    }
    else if (score >= 60) {
        cout << "Grade: D - Needs improvement" << endl;
    }
    else if (score >= 0) {
        cout << "Grade: F - Please study more" << endl;
    }
    else {
        cout << "Invalid score entered" << endl;
    }
    
    // Multiple conditions
    int age;
    bool hasLicense;
    
    cout << "\nEnter your age: ";
    cin >> age;
    cout << "Do you have a driver's license? (1 for yes, 0 for no): ";
    cin >> hasLicense;
    
    if (age >= 16 && hasLicense) {
        cout << "You can drive!" << endl;
    }
    else if (age >= 16 && !hasLicense) {
        cout << "You need to get a license first." << endl;
    }
    else {
        cout << "You're too young to drive." << endl;
    }
    
    return 0;
}
```

### switch Statement

```cpp
#include <iostream>
using namespace std;

int main() {
    char operation;
    double num1, num2;
    
    cout << "Enter two numbers: ";
    cin >> num1 >> num2;
    
    cout << "Enter operation (+, -, *, /): ";
    cin >> operation;
    
    switch (operation) {
        case '+':
            cout << num1 << " + " << num2 << " = " << (num1 + num2) << endl;
            break;
        case '-':
            cout << num1 << " - " << num2 << " = " << (num1 - num2) << endl;
            break;
        case '*':
            cout << num1 << " * " << num2 << " = " << (num1 * num2) << endl;
            break;
        case '/':
            if (num2 != 0) {
                cout << num1 << " / " << num2 << " = " << (num1 / num2) << endl;
            }
            else {
                cout << "Error: Division by zero!" << endl;
            }
            break;
        default:
            cout << "Error: Invalid operation!" << endl;
            break;
    }
    
    // Switch with multiple cases
    int dayNumber;
    cout << "\nEnter day number (1-7): ";
    cin >> dayNumber;
    
    switch (dayNumber) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            cout << "It's a weekday" << endl;
            break;
        case 6:
        case 7:
            cout << "It's weekend!" << endl;
            break;
        default:
            cout << "Invalid day number" << endl;
    }
    
    return 0;
}
```

### Ternary Operator

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 20;
    
    // Basic ternary operator: condition ? value_if_true : value_if_false
    int max = (a > b) ? a : b;
    cout << "Maximum of " << a << " and " << b << " is: " << max << endl;
    
    // Ternary with different data types
    int age = 18;
    string status = (age >= 18) ? "Adult" : "Minor";
    cout << "Status: " << status << endl;
    
    // Nested ternary (use sparingly)
    int score = 85;
    char grade = (score >= 90) ? 'A' : (score >= 80) ? 'B' : 'C';
    cout << "Grade: " << grade << endl;
    
    // Practical example
    int number = -5;
    cout << "The number " << number << " is " 
         << (number >= 0 ? "positive" : "negative") << endl;
    
    return 0;
}
```

---

## Loops

### for Loops

```cpp
#include <iostream>
using namespace std;

int main() {
    // Basic for loop
    cout << "Counting from 1 to 5:" << endl;
    for (int i = 1; i <= 5; i++) {
        cout << i << " ";
    }
    cout << endl;
    
    // Different increment values
    cout << "Even numbers from 0 to 10:" << endl;
    for (int i = 0; i <= 10; i += 2) {
        cout << i << " ";
    }
    cout << endl;
    
    // Counting backwards
    cout << "Countdown from 5 to 1:" << endl;
    for (int i = 5; i >= 1; i--) {
        cout << i << " ";
    }
    cout << endl;
    
    // Nested for loops
    cout << "\nMultiplication table (1-3):" << endl;
    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= 3; j++) {
            cout << i * j << "\t";
        }
        cout << endl;
    }
    
    // For loop with different initialization
    cout << "\nPattern printing:" << endl;
    for (int i = 1, j = 10; i <= 5; i++, j--) {
        cout << "i=" << i << ", j=" << j << endl;
    }
    
    return 0;
}
```

### while Loops

```cpp
#include <iostream>
using namespace std;

int main() {
    // Basic while loop
    int count = 1;
    cout << "While loop counting to 5:" << endl;
    while (count <= 5) {
        cout << count << " ";
        count++;
    }
    cout << endl;
    
    // Input validation with while
    int number;
    cout << "\nEnter a positive number: ";
    cin >> number;
    
    while (number <= 0) {
        cout << "Invalid! Enter a positive number: ";
        cin >> number;
    }
    cout << "You entered: " << number << endl;
    
    // Sentinel-controlled loop
    int sum = 0;
    int value;
    cout << "\nEnter numbers to sum (0 to stop):" << endl;
    
    cin >> value;
    while (value != 0) {
        sum += value;
        cin >> value;
    }
    cout << "Sum: " << sum << endl;
    
    return 0;
}
```

### do-while Loops

```cpp
#include <iostream>
using namespace std;

int main() {
    // Basic do-while loop
    int i = 1;
    cout << "Do-while loop:" << endl;
    do {
        cout << i << " ";
        i++;
    } while (i <= 5);
    cout << endl;
    
    // Menu-driven program
    int choice;
    do {
        cout << "\n--- Menu ---" << endl;
        cout << "1. Say Hello" << endl;
        cout << "2. Calculate Square" << endl;
        cout << "3. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;
        
        switch (choice) {
            case 1:
                cout << "Hello, World!" << endl;
                break;
            case 2: {
                int num;
                cout << "Enter a number: ";
                cin >> num;
                cout << "Square: " << num * num << endl;
                break;
            }
            case 3:
                cout << "Goodbye!" << endl;
                break;
            default:
                cout << "Invalid choice!" << endl;
        }
    } while (choice != 3);
    
    return 0;
}
```

### Loop Control Statements

```cpp
#include <iostream>
using namespace std;

int main() {
    // break statement
    cout << "Using break (stop at 3):" << endl;
    for (int i = 1; i <= 5; i++) {
        if (i == 3) {
            break;
        }
        cout << i << " ";
    }
    cout << endl;
    
    // continue statement
    cout << "Using continue (skip 3):" << endl;
    for (int i = 1; i <= 5; i++) {
        if (i == 3) {
            continue;
        }
        cout << i << " ";
    }
    cout << endl;
    
    // Finding prime numbers
    cout << "\nPrime numbers from 2 to 20:" << endl;
    for (int num = 2; num <= 20; num++) {
        bool isPrime = true;
        
        for (int i = 2; i * i <= num; i++) {
            if (num % i == 0) {
                isPrime = false;
                break; // Not prime, exit inner loop
            }
        }
        
        if (isPrime) {
            cout << num << " ";
        }
    }
    cout << endl;
    
    return 0;
}
```

---

## Functions

### Function Declaration and Definition

```cpp
#include <iostream>
using namespace std;

// Function declaration (prototype)
int add(int a, int b);
void printMessage();
double calculateArea(double radius);

int main() {
    // Function calls
    printMessage();
    
    int result = add(5, 3);
    cout << "5 + 3 = " << result << endl;
    
    double area = calculateArea(2.5);
    cout << "Area of circle with radius 2.5 = " << area << endl;
    
    return 0;
}

// Function definitions
void printMessage() {
    cout << "Hello from a function!" << endl;
}

int add(int a, int b) {
    return a + b;
}

double calculateArea(double radius) {
    const double PI = 3.14159;
    return PI * radius * radius;
}
```

### Function Parameters

```cpp
#include <iostream>
using namespace std;

// Pass by value
void passByValue(int x) {
    x = 100; // Changes local copy only
    cout << "Inside function: " << x << endl;
}

// Pass by reference
void passByReference(int& x) {
    x = 100; // Changes original variable
    cout << "Inside function: " << x << endl;
}

// Pass by pointer
void passByPointer(int* x) {
    *x = 100; // Changes value at address
    cout << "Inside function: " << *x << endl;
}

// Default parameters
void greet(string name, string greeting = "Hello") {
    cout << greeting << ", " << name << "!" << endl;
}

// Function overloading
int multiply(int a, int b) {
    return a * b;
}

double multiply(double a, double b) {
    return a * b;
}

int multiply(int a, int b, int c) {
    return a * b * c;
}

int main() {
    int value = 10;
    
    cout << "Original value: " << value << endl;
    
    passByValue(value);
    cout << "After pass by value: " << value << endl;
    
    passByReference(value);
    cout << "After pass by reference: " << value << endl;
    
    value = 50;
    passByPointer(&value);
    cout << "After pass by pointer: " << value << endl;
    
    // Default parameters
    greet("Alice");
    greet("Bob", "Hi");
    
    // Function overloading
    cout << multiply(3, 4) << endl;        // int version
    cout << multiply(3.5, 2.0) << endl;    // double version
    cout << multiply(2, 3, 4) << endl;     // three parameter version
    
    return 0;
}
```

### Recursive Functions

```cpp
#include <iostream>
using namespace std;

// Factorial calculation
long long factorial(int n) {
    if (n <= 1) {
        return 1; // Base case
    }
    return n * factorial(n - 1); // Recursive case
}

// Fibonacci sequence
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Power calculation
double power(double base, int exponent) {
    if (exponent == 0) {
        return 1;
    }
    if (exponent < 0) {
        return 1.0 / power(base, -exponent);
    }
    return base * power(base, exponent - 1);
}

int main() {
    int n = 5;
    cout << n << "! = " << factorial(n) << endl;
    
    cout << "First 10 Fibonacci numbers: ";
    for (int i = 0; i < 10; i++) {
        cout << fibonacci(i) << " ";
    }
    cout << endl;
    
    cout << "2^8 = " << power(2, 8) << endl;
    cout << "2^-3 = " << power(2, -3) << endl;
    
    return 0;
}
```

---

## Arrays and Vectors

### Arrays

```cpp
#include <iostream>
using namespace std;

int main() {
    // Array declaration and initialization
    int numbers[5] = {10, 20, 30, 40, 50};
    char vowels[] = {'a', 'e', 'i', 'o', 'u'}; // Size determined by initializer
    
    // Accessing array elements
    cout << "First number: " << numbers[0] << endl;
    cout << "Last number: " << numbers[4] << endl;
    
    // Modifying array elements
    numbers[2] = 35;
    cout << "Modified third number: " << numbers[2] << endl;
    
    // Looping through arrays
    cout << "All numbers: ";
    for (int i = 0; i < 5; i++) {
        cout << numbers[i] << " ";
    }
    cout << endl;
    
    // Range-based for loop (C++11)
    cout << "Vowels: ";
    for (char vowel : vowels) {
        cout << vowel << " ";
    }
    cout << endl;
    
    // Array size
    int arraySize = sizeof(numbers) / sizeof(numbers[0]);
    cout << "Array size: " << arraySize << endl;
    
    // Multi-dimensional arrays
    int matrix[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    cout << "Matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
    
    return 0;
}
```

### Vectors

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    // Vector declaration and initialization
    vector<int> numbers;                    // Empty vector
    vector<int> scores = {85, 92, 78, 96, 88}; // Initialize with values
    vector<string> names(3, "Unknown");    // 3 elements, all "Unknown"
    
    // Adding elements
    numbers.push_back(10);
    numbers.push_back(20);
    numbers.push_back(30);
    
    cout << "Numbers vector: ";
    for (int num : numbers) {
        cout << num << " ";
    }
    cout << endl;
    
    // Accessing elements
    cout << "First score: " << scores[0] << endl;
    cout << "Last score: " << scores.back() << endl;
    cout << "Score at index 2: " << scores.at(2) << endl; // Safe access with bounds checking
    
    // Vector properties
    cout << "Vector size: " << scores.size() << endl;
    cout << "Vector capacity: " << scores.capacity() << endl;
    cout << "Is empty: " << (numbers.empty() ? "Yes" : "No") << endl;
    
    // Modifying vectors
    scores[1] = 95;                         // Direct assignment
    scores.insert(scores.begin() + 2, 90);  // Insert at position 2
    scores.pop_back();                      // Remove last element
    
    cout << "Modified scores: ";
    for (size_t i = 0; i < scores.size(); i++) {
        cout << scores[i] << " ";
    }
    cout << endl;
    
    // Vector algorithms
    sort(scores.begin(), scores.end());     // Sort in ascending order
    cout << "Sorted scores: ";
    for (int score : scores) {
        cout << score << " ";
    }
    cout << endl;
    
    // Finding elements
    auto it = find(scores.begin(), scores.end(), 90);
    if (it != scores.end()) {
        cout << "Found 90 at position: " << (it - scores.begin()) << endl;
    }
    
    // Clear all elements
    numbers.clear();
    cout << "Numbers size after clear: " << numbers.size() << endl;
    
    return 0;
}
```

### Passing Arrays to Functions

```cpp
#include <iostream>
using namespace std;

// Function that takes array and size
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

// Function that modifies array elements
void doubleValues(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] *= 2;
    }
}

// Function working with vectors
void printVector(const vector<int>& vec) {
    for (int value : vec) {
        cout << value << " ";
    }
    cout << endl;
}

// Function that returns vector
vector<int> getRandomNumbers(int count) {
    vector<int> numbers;
    for (int i = 0; i < count; i++) {
        numbers.push_back(rand() % 100); // Random number 0-99
    }
    return numbers;
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    cout << "Original array: ";
    printArray(numbers, size);
    
    doubleValues(numbers, size);
    cout << "After doubling: ";
    printArray(numbers, size);
    
    // Working with vectors
    vector<int> scores = {85, 92, 78, 96};
    cout << "Vector: ";
    printVector(scores);
    
    vector<int> randomNums = getRandomNumbers(5);
    cout << "Random numbers: ";
    printVector(randomNums);
    
    return 0;
}
```

---

## Pointers and References

### Pointer Basics

```cpp
#include <iostream>
using namespace std;

int main() {
    int number = 42;
    int* ptr = &number;    // Pointer to number
    
    cout << "Value of number: " << number << endl;
    cout << "Address of number: " << &number << endl;
    cout << "Value of ptr: " << ptr << endl;
    cout << "Value pointed to by ptr: " << *ptr << endl;
    
    // Modifying value through pointer
    *ptr = 100;
    cout << "Number after modification through pointer: " << number << endl;
    
    // Pointer arithmetic
    int array[] = {10, 20, 30, 40, 50};
    int* arrPtr = array; // Points to first element
    
    cout << "\nArray elements using pointer arithmetic:" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "Element " << i << ": " << *(arrPtr + i) << endl;
    }
    
    // Null pointer
    int* nullPtr = nullptr;
    if (nullPtr == nullptr) {
        cout << "Pointer is null" << endl;
    }
    
    return 0;
}
```

### Dynamic Memory Allocation

```cpp
#include <iostream>
using namespace std;

int main() {
    // Allocate single integer
    int* dynamicInt = new int(25);
    cout << "Dynamic integer: " << *dynamicInt << endl;
    
    // Allocate array
    int size = 5;
    int* dynamicArray = new int[size];
    
    // Initialize array
    for (int i = 0; i < size; i++) {
        dynamicArray[i] = (i + 1) * 10;
    }
    
    cout << "Dynamic array: ";
    for (int i = 0; i < size; i++) {
        cout << dynamicArray[i] << " ";
    }
    cout << endl;
    
    // Don't forget to free memory!
    delete dynamicInt;
    delete[] dynamicArray;
    
    // Set pointers to null after deletion
    dynamicInt = nullptr;
    dynamicArray = nullptr;
    
    return 0;
}
```

### References

```cpp
#include <iostream>
using namespace std;

// Function using references
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int original = 10;
    int& reference = original; // Reference to original
    
    cout << "Original: " << original << endl;
    cout << "Reference: " << reference << endl;
    
    reference = 20; // Modifies original
    cout << "After modifying reference:" << endl;
    cout << "Original: " << original << endl;
    cout << "Reference: " << reference << endl;
    
    // Using references in functions
    int x = 5, y = 10;
    cout << "\nBefore swap: x = " << x << ", y = " << y << endl;
    swap(x, y);
    cout << "After swap: x = " << x << ", y = " << y << endl;
    
    // Reference vs Pointer
    int value = 42;
    int& ref = value;     // Reference (alias)
    int* ptr = &value;    // Pointer (address)
    
    cout << "\nComparison:" << endl;
    cout << "Value: " << value << endl;
    cout << "Reference: " << ref << endl;
    cout << "Pointer: " << *ptr << endl;
    
    return 0;
}
```

---

## Classes and Objects

### Basic Class Definition

```cpp
#include <iostream>
#include <string>
using namespace std;

class Student {
private:
    string name;
    int age;
    double gpa;

public:
    // Constructor
    Student(string n, int a, double g) {
        name = n;
        age = a;
        gpa = g;
    }
    
    // Default constructor
    Student() {
        name = "Unknown";
        age = 0;
        gpa = 0.0;
    }
    
    // Getter methods
    string getName() const {
        return name;
    }
    
    int getAge() const {
        return age;
    }
    
    double getGPA() const {
        return gpa;
    }
    
    // Setter methods
    void setName(string n) {
        name = n;
    }
    
    void setAge(int a) {
        if (a >= 0) {
            age = a;
        }
    }
    
    void setGPA(double g) {
        if (g >= 0.0 && g <= 4.0) {
            gpa = g;
        }
    }
    
    // Method to display student information
    void displayInfo() const {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "GPA: " << gpa << endl;
    }
    
    // Method to check if student is on honor roll
    bool isHonorRoll() const {
        return gpa >= 3.5;
    }
};

int main() {
    // Creating objects
    Student student1("Alice", 20, 3.8);
    Student student2; // Uses default constructor
    
    // Using methods
    student1.displayInfo();
    cout << "Honor roll: " << (student1.isHonorRoll() ? "Yes" : "No") << endl;
    
    cout << "\n";
    
    // Modifying object
    student2.setName("Bob");
    student2.setAge(19);
    student2.setGPA(3.2);
    student2.displayInfo();
    
    return 0;
}
```

### Constructor and Destructor

```cpp
#include <iostream>
#include <string>
using namespace std;

class BankAccount {
private:
    string accountNumber;
    string ownerName;
    double balance;

public:
    // Parameterized constructor
    BankAccount(string accNum, string owner, double initialBalance = 0.0) {
        accountNumber = accNum;
        ownerName = owner;
        balance = initialBalance;
        cout << "Account created for " << ownerName << endl;
    }
    
    // Copy constructor
    BankAccount(const BankAccount& other) {
        accountNumber = other.accountNumber + "_COPY";
        ownerName = other.ownerName;
        balance = other.balance;
        cout << "Copy of account created" << endl;
    }
    
    // Destructor
    ~BankAccount() {
        cout << "Account " << accountNumber << " destroyed" << endl;
    }
    
    // Methods
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            cout << "Deposited $" << amount << ". New balance: $" << balance << endl;
        }
    }
    
    bool withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            cout << "Withdrew $" << amount << ". New balance: $" << balance << endl;
            return true;
        }
        cout << "Insufficient funds or invalid amount" << endl;
        return false;
    }
    
    double getBalance() const {
        return balance;
    }
    
    void displayAccount() const {
        cout << "Account: " << accountNumber << endl;
        cout << "Owner: " << ownerName << endl;
        cout << "Balance: $" << balance << endl;
    }
};

int main() {
    // Creating objects
    BankAccount account1("ACC001", "Alice", 1000.0);
    account1.displayAccount();
    
    // Using methods
    account1.deposit(500.0);
    account1.withdraw(200.0);
    
    cout << "\n";
    
    // Copy constructor
    BankAccount account2 = account1;
    account2.displayAccount();
    
    return 0;
} // Destructors called automatically when objects go out of scope
```

### Static Members and Methods

```cpp
#include <iostream>
#include <string>
using namespace std;

class Counter {
private:
    static int totalObjects; // Static member variable
    int objectId;

public:
    Counter() {
        totalObjects++;
        objectId = totalObjects;
        cout << "Object " << objectId << " created" << endl;
    }
    
    ~Counter() {
        cout << "Object " << objectId << " destroyed" << endl;
    }
    
    // Static method
    static int getTotalObjects() {
        return totalObjects;
    }
    
    void displayId() const {
        cout << "Object ID: " << objectId << endl;
    }
};

// Initialize static member
int Counter::totalObjects = 0;

int main() {
    cout << "Initial count: " << Counter::getTotalObjects() << endl;
    
    Counter obj1;
    Counter obj2;
    Counter obj3;
    
    cout << "Current count: " << Counter::getTotalObjects() << endl;
    
    obj1.displayId();
    obj2.displayId();
    obj3.displayId();
    
    return 0;
}
```

---

## String Manipulation

### String Basics

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // String creation
    string str1 = "Hello";
    string str2("World");
    string str3(5, 'A'); // "AAAAA"
    string str4 = str1;  // Copy constructor
    
    cout << "str1: " << str1 << endl;
    cout << "str2: " << str2 << endl;
    cout << "str3: " << str3 << endl;
    cout << "str4: " << str4 << endl;
    
    // String concatenation
    string greeting = str1 + ", " + str2 + "!";
    cout << "Greeting: " << greeting << endl;
    
    // String properties
    cout << "Length of greeting: " << greeting.length() << endl;
    cout << "Size of greeting: " << greeting.size() << endl;
    cout << "Is empty: " << (greeting.empty() ? "Yes" : "No") << endl;
    
    // Accessing characters
    cout << "First character: " << greeting[0] << endl;
    cout << "Last character: " << greeting[greeting.length() - 1] << endl;
    cout << "Character at index 7: " << greeting.at(7) << endl;
    
    return 0;
}
```

### String Operations

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string text = "The Quick Brown Fox Jumps Over The Lazy Dog";
    cout << "Original: " << text << endl;
    
    // Case conversion
    string upperText = text;
    transform(upperText.begin(), upperText.end(), upperText.begin(), ::toupper);
    cout << "Uppercase: " << upperText << endl;
    
    string lowerText = text;
    transform(lowerText.begin(), lowerText.end(), lowerText.begin(), ::tolower);
    cout << "Lowercase: " << lowerText << endl;
    
    // Substring operations
    string substring = text.substr(4, 5); // Starting at index 4, length 5
    cout << "Substring (4, 5): " << substring << endl;
    
    // Finding substrings
    size_t pos = text.find("Fox");
    if (pos != string::npos) {
        cout << "Found 'Fox' at position: " << pos << endl;
    }
    
    // Replace operations
    string replaced = text;
    replaced.replace(pos, 3, "Cat"); // Replace "Fox" with "Cat"
    cout << "After replacement: " << replaced << endl;
    
    // Insert and erase
    string modified = text;
    modified.insert(4, "Very ");
    cout << "After insert: " << modified << endl;
    
    modified.erase(4, 5); // Remove "Very "
    cout << "After erase: " << modified << endl;
    
    // String comparison
    string str1 = "apple";
    string str2 = "banana";
    
    if (str1 < str2) {
        cout << str1 << " comes before " << str2 << " alphabetically" << endl;
    }
    
    return 0;
}
```

### String Input and Parsing

```cpp
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
using namespace std;

int main() {
    // Reading entire line
    string fullName;
    cout << "Enter your full name: ";
    getline(cin, fullName);
    cout << "Hello, " << fullName << "!" << endl;
    
    // Parsing comma-separated values
    string csvData = "Alice,25,Engineer,New York";
    stringstream ss(csvData);
    string item;
    vector<string> tokens;
    
    while (getline(ss, item, ',')) {
        tokens.push_back(item);
    }
    
    cout << "\nParsed data:" << endl;
    for (size_t i = 0; i < tokens.size(); i++) {
        cout << "Token " << i << ": " << tokens[i] << endl;
    }
    
    // Converting strings to numbers
    string numberStr = "123";
    string floatStr = "45.67";
    
    int number = stoi(numberStr);       // string to int
    double decimal = stod(floatStr);    // string to double
    
    cout << "\nConverted numbers:" << endl;
    cout << "Integer: " << number << endl;
    cout << "Double: " << decimal << endl;
    
    // Converting numbers to strings
    int value = 789;
    string valueStr = to_string(value);
    cout << "Number as string: " << valueStr << endl;
    
    return 0;
}
```

---

## File Operations

### Reading from Files

```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    // Reading entire file
    ifstream inputFile("data.txt");
    
    if (inputFile.is_open()) {
        string line;
        cout << "File contents:" << endl;
        
        while (getline(inputFile, line)) {
            cout << line << endl;
        }
        
        inputFile.close();
    }
    else {
        cout << "Unable to open file" << endl;
    }
    
    // Reading specific data types
    ifstream dataFile("numbers.txt");
    if (dataFile.is_open()) {
        int number;
        double decimal;
        string word;
        
        dataFile >> number >> decimal >> word;
        
        cout << "\nRead from file:" << endl;
        cout << "Number: " << number << endl;
        cout << "Decimal: " << decimal << endl;
        cout << "Word: " << word << endl;
        
        dataFile.close();
    }
    
    return 0;
}
```

### Writing to Files

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int main() {
    // Writing to file (overwrite mode)
    ofstream outputFile("output.txt");
    
    if (outputFile.is_open()) {
        outputFile << "Hello, File!" << endl;
        outputFile << "This is line 2" << endl;
        outputFile << "Number: " << 42 << endl;
        outputFile.close();
        cout << "Data written to output.txt" << endl;
    }
    
    // Appending to file
    ofstream appendFile("output.txt", ios::app);
    if (appendFile.is_open()) {
        appendFile << "This line was appended" << endl;
        appendFile.close();
        cout << "Data appended to output.txt" << endl;
    }
    
    // Writing student records
    vector<string> students = {"Alice", "Bob", "Charlie"};
    vector<int> grades = {85, 92, 78};
    
    ofstream gradesFile("grades.txt");
    if (gradesFile.is_open()) {
        gradesFile << "Student Grades Report" << endl;
        gradesFile << "=====================" << endl;
        
        for (size_t i = 0; i < students.size(); i++) {
            gradesFile << students[i] << ": " << grades[i] << endl;
        }
        
        gradesFile.close();
        cout << "Grades written to grades.txt" << endl;
    }
    
    return 0;
}
```

### File Error Handling

```cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

bool copyFile(const string& source, const string& destination) {
    ifstream src(source, ios::binary);
    ofstream dest(destination, ios::binary);
    
    if (!src.is_open()) {
        cout << "Error: Could not open source file " << source << endl;
        return false;
    }
    
    if (!dest.is_open()) {
        cout << "Error: Could not create destination file " << destination << endl;
        return false;
    }
    
    // Copy file contents
    dest << src.rdbuf();
    
    src.close();
    dest.close();
    
    return true;
}

int main() {
    string filename = "test.txt";
    
    // Check if file exists and read it
    ifstream file(filename);
    if (file.good()) {
        cout << "File exists and is readable" << endl;
        
        string line;
        while (getline(file, line)) {
            cout << line << endl;
        }
        
        if (file.eof()) {
            cout << "Reached end of file successfully" << endl;
        }
        else if (file.fail()) {
            cout << "Error occurred while reading file" << endl;
        }
        
        file.close();
    }
    else {
        cout << "File does not exist or cannot be opened" << endl;
        
        // Create the file
        ofstream newFile(filename);
        if (newFile.is_open()) {
            newFile << "This is a new file" << endl;
            newFile << "Created by the program" << endl;
            newFile.close();
            cout << "File created successfully" << endl;
        }
    }
    
    // Copy file example
    if (copyFile("test.txt", "backup.txt")) {
        cout << "File copied successfully" << endl;
    }
    else {
        cout << "File copy failed" << endl;
    }
    
    return 0;
}
```

---

## Memory Management

### Stack vs Heap

```cpp
#include <iostream>
using namespace std;

int main() {
    // Stack allocation (automatic)
    int stackVar = 10;
    int stackArray[5] = {1, 2, 3, 4, 5};
    
    cout << "Stack variable: " << stackVar << endl;
    cout << "Stack array: ";
    for (int i = 0; i < 5; i++) {
        cout << stackArray[i] << " ";
    }
    cout << endl;
    
    // Heap allocation (dynamic)
    int* heapVar = new int(20);
    int* heapArray = new int[5];
    
    // Initialize heap array
    for (int i = 0; i < 5; i++) {
        heapArray[i] = (i + 1) * 10;
    }
    
    cout << "Heap variable: " << *heapVar << endl;
    cout << "Heap array: ";
    for (int i = 0; i < 5; i++) {
        cout << heapArray[i] << " ";
    }
    cout << endl;
    
    // Don't forget to free heap memory!
    delete heapVar;
    delete[] heapArray;
    
    // Set pointers to null
    heapVar = nullptr;
    heapArray = nullptr;
    
    return 0;
} // Stack variables automatically destroyed here
```

### Smart Pointers (C++11)

```cpp
#include <iostream>
#include <memory>
#include <vector>
using namespace std;

class Resource {
private:
    string name;

public:
    Resource(string n) : name(n) {
        cout << "Resource " << name << " created" << endl;
    }
    
    ~Resource() {
        cout << "Resource " << name << " destroyed" << endl;
    }
    
    void use() {
        cout << "Using resource " << name << endl;
    }
};

int main() {
    // unique_ptr - exclusive ownership
    {
        unique_ptr<Resource> ptr1 = make_unique<Resource>("Resource1");
        ptr1->use();
        
        // Transfer ownership
        unique_ptr<Resource> ptr2 = move(ptr1);
        if (ptr1 == nullptr) {
            cout << "ptr1 is now null" << endl;
        }
        ptr2->use();
    } // Resource automatically destroyed when unique_ptr goes out of scope
    
    cout << endl;
    
    // shared_ptr - shared ownership
    {
        shared_ptr<Resource> shared1 = make_shared<Resource>("Resource2");
        cout << "Reference count: " << shared1.use_count() << endl;
        
        {
            shared_ptr<Resource> shared2 = shared1;
            cout << "Reference count: " << shared1.use_count() << endl;
            shared2->use();
        } // shared2 destroyed, but Resource2 still exists
        
        cout << "Reference count: " << shared1.use_count() << endl;
        shared1->use();
    } // Resource2 destroyed when last shared_ptr is destroyed
    
    // Using smart pointers with containers
    vector<unique_ptr<Resource>> resources;
    resources.push_back(make_unique<Resource>("Resource3"));
    resources.push_back(make_unique<Resource>("Resource4"));
    
    for (auto& resource : resources) {
        resource->use();
    }
    
    return 0;
}
```

---

## Practice Exercises

### Exercise 1: Student Grade Manager

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>
using namespace std;

class Student {
private:
    string name;
    vector<double> grades;

public:
    Student(string n) : name(n) {}
    
    void addGrade(double grade) {
        if (grade >= 0 && grade <= 100) {
            grades.push_back(grade);
        }
    }
    
    double getAverage() const {
        if (grades.empty()) return 0;
        
        double sum = 0;
        for (double grade : grades) {
            sum += grade;
        }
        return sum / grades.size();
    }
    
    char getLetterGrade() const {
        double avg = getAverage();
        if (avg >= 90) return 'A';
        if (avg >= 80) return 'B';
        if (avg >= 70) return 'C';
        if (avg >= 60) return 'D';
        return 'F';
    }
    
    string getName() const { return name; }
    
    void displayInfo() const {
        cout << "Student: " << name << endl;
        cout << "Grades: ";
        for (double grade : grades) {
            cout << grade << " ";
        }
        cout << endl;
        cout << "Average: " << getAverage() << endl;
        cout << "Letter Grade: " << getLetterGrade() << endl;
    }
    
    void saveToFile(ofstream& file) const {
        file << name << ",";
        for (size_t i = 0; i < grades.size(); i++) {
            file << grades[i];
            if (i < grades.size() - 1) file << ",";
        }
        file << endl;
    }
};

class GradeManager {
private:
    vector<Student> students;

public:
    void addStudent(const string& name) {
        students.push_back(Student(name));
    }
    
    void addGradeToStudent(const string& name, double grade) {
        for (Student& student : students) {
            if (student.getName() == name) {
                student.addGrade(grade);
                return;
            }
        }
        cout << "Student not found!" << endl;
    }
    
    void displayAllStudents() const {
        for (const Student& student : students) {
            student.displayInfo();
            cout << "-------------------" << endl;
        }
    }
    
    void saveToFile(const string& filename) const {
        ofstream file(filename);
        if (file.is_open()) {
            for (const Student& student : students) {
                student.saveToFile(file);
            }
            file.close();
            cout << "Data saved to " << filename << endl;
        }
    }
};

int main() {
    GradeManager manager;
    
    // Add students
    manager.addStudent("Alice");
    manager.addStudent("Bob");
    manager.addStudent("Charlie");
    
    // Add grades
    manager.addGradeToStudent("Alice", 85);
    manager.addGradeToStudent("Alice", 92);
    manager.addGradeToStudent("Alice", 78);
    
    manager.addGradeToStudent("Bob", 90);
    manager.addGradeToStudent("Bob", 87);
    
    manager.addGradeToStudent("Charlie", 95);
    manager.addGradeToStudent("Charlie", 98);
    manager.addGradeToStudent("Charlie", 91);
    
    // Display all students
    manager.displayAllStudents();
    
    // Save to file
    manager.saveToFile("grades.csv");
    
    return 0;
}
```

### Exercise 2: Simple Banking System

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <memory>
using namespace std;

class Transaction {
private:
    string type;
    double amount;
    string date;

public:
    Transaction(string t, double a, string d) : type(t), amount(a), date(d) {}
    
    void display() const {
        cout << date << " - " << type << ": $" << amount << endl;
    }
    
    double getAmount() const { return amount; }
    string getType() const { return type; }
};

class BankAccount {
private:
    string accountNumber;
    string ownerName;
    double balance;
    vector<unique_ptr<Transaction>> transactions;

public:
    BankAccount(string accNum, string owner, double initialBalance = 0) 
        : accountNumber(accNum), ownerName(owner), balance(initialBalance) {
        if (initialBalance > 0) {
            transactions.push_back(make_unique<Transaction>("Initial Deposit", initialBalance, "2024-01-01"));
        }
    }
    
    bool deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            transactions.push_back(make_unique<Transaction>("Deposit", amount, "2024-01-01"));
            return true;
        }
        return false;
    }
    
    bool withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            transactions.push_back(make_unique<Transaction>("Withdrawal", amount, "2024-01-01"));
            return true;
        }
        return false;
    }
    
    double getBalance() const { return balance; }
    string getAccountNumber() const { return accountNumber; }
    string getOwnerName() const { return ownerName; }
    
    void displayAccountInfo() const {
        cout << "Account Number: " << accountNumber << endl;
        cout << "Owner: " << ownerName << endl;
        cout << "Balance: $" << balance << endl;
    }
    
    void displayTransactionHistory() const {
        cout << "Transaction History for " << accountNumber << ":" << endl;
        for (const auto& transaction : transactions) {
            transaction->display();
        }
    }
};

class Bank {
private:
    vector<unique_ptr<BankAccount>> accounts;
    
public:
    void createAccount(const string& accountNumber, const string& ownerName, double initialDeposit = 0) {
        accounts.push_back(make_unique<BankAccount>(accountNumber, ownerName, initialDeposit));
        cout << "Account created successfully!" << endl;
    }
    
    BankAccount* findAccount(const string& accountNumber) {
        for (auto& account : accounts) {
            if (account->getAccountNumber() == accountNumber) {
                return account.get();
            }
        }
        return nullptr;
    }
    
    void displayAllAccounts() const {
        cout << "All Bank Accounts:" << endl;
        cout << "==================" << endl;
        for (const auto& account : accounts) {
            account->displayAccountInfo();
            cout << "-------------------" << endl;
        }
    }
    
    bool transferMoney(const string& fromAccount, const string& toAccount, double amount) {
        BankAccount* from = findAccount(fromAccount);
        BankAccount* to = findAccount(toAccount);
        
        if (from && to && from->withdraw(amount)) {
            to->deposit(amount);
            cout << "Transfer successful!" << endl;
            return true;
        }
        cout << "Transfer failed!" << endl;
        return false;
    }
};

void displayMenu() {
    cout << "\n=== Banking System ===" << endl;
    cout << "1. Create Account" << endl;
    cout << "2. Deposit Money" << endl;
    cout << "3. Withdraw Money" << endl;
    cout << "4. Check Balance" << endl;
    cout << "5. Transfer Money" << endl;
    cout << "6. View Transaction History" << endl;
    cout << "7. Display All Accounts" << endl;
    cout << "8. Exit" << endl;
    cout << "Enter your choice: ";
}

int main() {
    Bank bank;
    int choice;
    
    do {
        displayMenu();
        cin >> choice;
        
        switch (choice) {
            case 1: {
                string accNum, name;
                double initial;
                cout << "Enter account number: ";
                cin >> accNum;
                cout << "Enter owner name: ";
                cin.ignore();
                getline(cin, name);
                cout << "Enter initial deposit: ";
                cin >> initial;
                bank.createAccount(accNum, name, initial);
                break;
            }
            case 2: {
                string accNum;
                double amount;
                cout << "Enter account number: ";
                cin >> accNum;
                cout << "Enter deposit amount: ";
                cin >> amount;
                
                BankAccount* account = bank.findAccount(accNum);
                if (account && account->deposit(amount)) {
                    cout << "Deposit successful! New balance: $" << account->getBalance() << endl;
                } else {
                    cout << "Deposit failed!" << endl;
                }
                break;
            }
            case 3: {
                string accNum;
                double amount;
                cout << "Enter account number: ";
                cin >> accNum;
                cout << "Enter withdrawal amount: ";
                cin >> amount;
                
                BankAccount* account = bank.findAccount(accNum);
                if (account && account->withdraw(amount)) {
                    cout << "Withdrawal successful! New balance: $" << account->getBalance() << endl;
                } else {
                    cout << "Withdrawal failed!" << endl;
                }
                break;
            }
            case 4: {
                string accNum;
                cout << "Enter account number: ";
                cin >> accNum;
                
                BankAccount* account = bank.findAccount(accNum);
                if (account) {
                    cout << "Current balance: $" << account->getBalance() << endl;
                } else {
                    cout << "Account not found!" << endl;
                }
                break;
            }
            case 5: {
                string fromAcc, toAcc;
                double amount;
                cout << "Enter source account: ";
                cin >> fromAcc;
                cout << "Enter destination account: ";
                cin >> toAcc;
                cout << "Enter transfer amount: ";
                cin >> amount;
                
                bank.transferMoney(fromAcc, toAcc, amount);
                break;
            }
            case 6: {
                string accNum;
                cout << "Enter account number: ";
                cin >> accNum;
                
                BankAccount* account = bank.findAccount(accNum);
                if (account) {
                    account->displayTransactionHistory();
                } else {
                    cout << "Account not found!" << endl;
                }
                break;
            }
            case 7:
                bank.displayAllAccounts();
                break;
            case 8:
                cout << "Thank you for using our banking system!" << endl;
                break;
            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    } while (choice != 8);
    
    return 0;
}
```

### Exercise 3: Text File Analyzer

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <sstream>
using namespace std;

class TextAnalyzer {
private:
    map<string, int> wordCount;
    int totalWords;
    int totalLines;
    int totalCharacters;
    
    string cleanWord(const string& word) {
        string cleaned;
        for (char c : word) {
            if (isalnum(c)) {
                cleaned += tolower(c);
            }
        }
        return cleaned;
    }

public:
    TextAnalyzer() : totalWords(0), totalLines(0), totalCharacters(0) {}
    
    bool analyzeFile(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "Error: Cannot open file " << filename << endl;
            return false;
        }
        
        string line;
        while (getline(file, line)) {
            totalLines++;
            totalCharacters += line.length();
            
            // Parse words from line
            stringstream ss(line);
            string word;
            while (ss >> word) {
                string cleanedWord = cleanWord(word);
                if (!cleanedWord.empty()) {
                    wordCount[cleanedWord]++;
                    totalWords++;
                }
            }
        }
        
        file.close();
        return true;
    }
    
    void displayStatistics() const {
        cout << "=== Text Analysis Results ===" << endl;
        cout << "Total lines: " << totalLines << endl;
        cout << "Total words: " << totalWords << endl;
        cout << "Total characters: " << totalCharacters << endl;
        cout << "Unique words: " << wordCount.size() << endl;
        cout << "Average words per line: " << (totalLines > 0 ? (double)totalWords / totalLines : 0) << endl;
    }
    
    void displayTopWords(int count = 10) const {
        // Create vector of pairs for sorting
        vector<pair<string, int>> wordPairs(wordCount.begin(), wordCount.end());
        
        // Sort by frequency (descending)
        sort(wordPairs.begin(), wordPairs.end(), 
             [](const pair<string, int>& a, const pair<string, int>& b) {
                 return a.second > b.second;
             });
        
        cout << "\n=== Top " << count << " Most Frequent Words ===" << endl;
        for (int i = 0; i < min(count, (int)wordPairs.size()); i++) {
            cout << i + 1 << ". " << wordPairs[i].first 
                 << " (" << wordPairs[i].second << " times)" << endl;
        }
    }
    
    void findWord(const string& word) const {
        string cleanedWord = cleanWord(word);
        auto it = wordCount.find(cleanedWord);
        if (it != wordCount.end()) {
            cout << "Word '" << word << "' appears " << it->second << " times" << endl;
        } else {
            cout << "Word '" << word << "' not found" << endl;
        }
    }
    
    void saveReport(const string& filename) const {
        ofstream file(filename);
        if (file.is_open()) {
            file << "Text Analysis Report" << endl;
            file << "===================" << endl;
            file << "Total lines: " << totalLines << endl;
            file << "Total words: " << totalWords << endl;
            file << "Total characters: " << totalCharacters << endl;
            file << "Unique words: " << wordCount.size() << endl;
            file << endl;
            
            file << "Word Frequency List:" << endl;
            
            // Create sorted list
            vector<pair<string, int>> wordPairs(wordCount.begin(), wordCount.end());
            sort(wordPairs.begin(), wordPairs.end());
            
            for (const auto& pair : wordPairs) {
                file << pair.first << ": " << pair.second << endl;
            }
            
            file.close();
            cout << "Report saved to " << filename << endl;
        }
    }
};

int main() {
    TextAnalyzer analyzer;
    string filename;
    
    cout << "Enter filename to analyze: ";
    cin >> filename;
    
    if (analyzer.analyzeFile(filename)) {
        int choice;
        do {
            cout << "\n=== Text Analyzer Menu ===" << endl;
            cout << "1. Display Statistics" << endl;
            cout << "2. Show Top Words" << endl;
            cout << "3. Find Specific Word" << endl;
            cout << "4. Save Report" << endl;
            cout << "5. Exit" << endl;
            cout << "Enter your choice: ";
            cin >> choice;
            
            switch (choice) {
                case 1:
                    analyzer.displayStatistics();
                    break;
                case 2: {
                    int count;
                    cout << "How many top words to display? ";
                    cin >> count;
                    analyzer.displayTopWords(count);
                    break;
                }
                case 3: {
                    string word;
                    cout << "Enter word to find: ";
                    cin >> word;
                    analyzer.findWord(word);
                    break;
                }
                case 4: {
                    string reportFile;
                    cout << "Enter report filename: ";
                    cin >> reportFile;
                    analyzer.saveReport(reportFile);
                    break;
                }
                case 5:
                    cout << "Goodbye!" << endl;
                    break;
                default:
                    cout << "Invalid choice!" << endl;
            }
        } while (choice != 5);
    }
    
    return 0;
}
```

---

## Summary

These notes cover the fundamental concepts of C++ programming:

1. **Program Structure**: Understanding compilation, headers, and namespaces
2. **Variables and Data Types**: Working with different data types and type conversion
3. **Operations**: Arithmetic, comparison, and logical operations
4. **Control Flow**: Making decisions and repeating actions with conditions and loops
5. **Functions**: Organizing code into reusable blocks with parameters and return values
6. **Arrays and Vectors**: Working with collections of data
7. **Pointers and References**: Understanding memory addresses and references
8. **Classes and Objects**: Object-oriented programming fundamentals
9. **String Manipulation**: Processing and formatting text
10. **File Operations**: Reading from and writing to files
11. **Memory Management**: Stack vs heap allocation and smart pointers

### Key C++ Features

- **Strong Type System**: Compile-time type checking prevents many errors
- **Object-Oriented Programming**: Encapsulation, inheritance, and polymorphism
- **Manual Memory Management**: Direct control over memory allocation
- **Performance**: Compiled to efficient machine code
- **Standard Template Library (STL)**: Rich collection of containers and algorithms

### Best Practices

1. **Use meaningful variable names** and follow naming conventions
2. **Initialize variables** when declaring them
3. **Use const** for values that shouldn't change
4. **Prefer vectors over arrays** for dynamic data
5. **Use smart pointers** instead of raw pointers when possible
6. **Handle errors gracefully** with proper error checking
7. **Comment your code** to explain complex logic
8. **Follow RAII** (Resource Acquisition Is Initialization) principle

### Next Steps

1. Practice with the provided exercises
2. Learn about inheritance and polymorphism
3. Explore the Standard Template Library (STL)
4. Study advanced topics like templates and exception handling
5. Work on larger projects to apply these concepts
6. Learn modern C++ features (C++11, C++14, C++17, C++20)

### Additional Resources

- **C++ Reference**: https://cppreference.com/
- **Books**: "C++ Primer" by Lippman, "Effective C++" by Meyers
- **Online Compilers**: Compiler Explorer, Online GDB
- **Practice**: HackerRank, LeetCode, Codeforces

Remember: C++ is a powerful language that requires practice to master. Start with simple programs and gradually work your way up to more complex applications!