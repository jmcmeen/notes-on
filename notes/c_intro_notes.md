# Elementary C Programming Concepts

## Table of Contents

1. [Getting Started with C](#getting-started-with-c)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Arrays](#arrays)
9. [Pointers](#pointers)
10. [Strings](#strings)
11. [Structures](#structures)
12. [Memory Management](#memory-management)
13. [File Operations](#file-operations)
14. [Preprocessor and Header Files](#preprocessor-and-header-files)
15. [Practice Exercises](#practice-exercises)

---

## Getting Started with C

### What is C?

C is a general-purpose, procedural programming language created by Dennis Ritchie at Bell Labs in 1972. Key characteristics:
- **Low-level access**: Direct memory manipulation via pointers
- **Compiled language**: Source code is translated to machine code for fast execution
- **Portable**: C programs can be compiled on virtually any platform
- **Minimal runtime**: No garbage collector, small standard library
- **Foundational**: Influenced C++, Java, C#, Go, Rust, and many others
- **System programming**: Used for operating systems, embedded systems, and compilers

### Your First C Program

```c
#include <stdio.h>

int main(void) {
    // This is a comment
    printf("Hello, World!\n");
    return 0;
}
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **#include <stdio.h>** - Includes the Standard I/O library for `printf`, `scanf`, etc.
- **int main(void)** - Entry point of the program; returns an integer status code
- **printf()** - Prints formatted text to the console
- **\n** - Newline character
- **return 0;** - Indicates successful execution (non-zero means error)
- **//** - Single-line comment (C99+)
- **/* ... */** - Multi-line comment

### Compiling and Running

```bash
gcc hello.c -o hello    # Compile with GCC
./hello                 # Run the compiled program

gcc -Wall -Wextra -std=c11 hello.c -o hello  # With warnings and C11 standard
```

### Development Environment

- **GCC**: GNU Compiler Collection (most common on Linux/Mac)
- **Clang**: Alternative compiler with excellent error messages
- **MSVC**: Microsoft Visual C++ compiler (Windows)
- **VS Code**: Lightweight editor with C/C++ extensions
- **CLion**: Full-featured IDE from JetBrains

---

## Variables and Data Types

### Variable Declaration

In C, you must declare variables with their type before using them. In C89/90, declarations must be at the top of a block; C99+ allows declarations anywhere.

```c
#include <stdio.h>

int main(void) {
    // Declaring variables
    char grade = 'A';
    int age = 25;
    float height = 5.6f;
    double price = 19.99;

    printf("Grade: %c\n", grade);
    printf("Age: %d\n", age);
    printf("Height: %.1f\n", height);
    printf("Price: %.2f\n", price);

    return 0;
}
```

### Basic Data Types

#### 1. Integer Types
```c
// Different integer types
char smallNum = 127;               // At least 8 bits (-128 to 127)
short shortNum = 32000;            // At least 16 bits
int number = 2000000;              // At least 16 bits (usually 32)
long bigNum = 2000000000L;         // At least 32 bits
long long veryBig = 9000000000LL;  // At least 64 bits (C99+)

// Unsigned variants (no negative values, double the positive range)
unsigned int positive = 4000000000U;
unsigned char byte = 255;

printf("int: %d\n", number);
printf("long: %ld\n", bigNum);
printf("long long: %lld\n", veryBig);
printf("unsigned: %u\n", positive);
```

#### 2. Floating Point Types
```c
// Decimal numbers
float pi = 3.14f;           // ~7 digits precision (suffix f)
double precise = 3.14159265358979;  // ~15 digits precision
long double extra = 3.14159265358979323846L; // Extended precision

printf("float: %f\n", pi);
printf("double: %lf\n", precise);
printf("2 decimals: %.2f\n", pi);
```

#### 3. Character Type
```c
// Characters are stored as integers (ASCII values)
char letter = 'A';
char newline = '\n';
char tab = '\t';

printf("Character: %c\n", letter);
printf("ASCII value: %d\n", letter);  // 65

// Character arithmetic
char next = letter + 1;  // 'B'
printf("Next letter: %c\n", next);
```

#### 4. Boolean Type (C99+)
```c
#include <stdbool.h>

bool isRaining = false;
bool isSunny = true;
bool result = 5 > 3;  // true

printf("Is raining: %d\n", isRaining);  // 0
printf("5 > 3: %d\n", result);          // 1

// Without stdbool.h, any non-zero value is "true"
int flag = 1;  // true
if (flag) {
    printf("Flag is true\n");
}
```

### sizeof Operator

```c
#include <stdio.h>

int main(void) {
    printf("char:      %zu bytes\n", sizeof(char));
    printf("short:     %zu bytes\n", sizeof(short));
    printf("int:       %zu bytes\n", sizeof(int));
    printf("long:      %zu bytes\n", sizeof(long));
    printf("long long: %zu bytes\n", sizeof(long long));
    printf("float:     %zu bytes\n", sizeof(float));
    printf("double:    %zu bytes\n", sizeof(double));
    printf("pointer:   %zu bytes\n", sizeof(int *));

    return 0;
}
```

### Variable Initialization and Constants

```c
// Different ways to declare and initialize
int a = 10;                  // Declaration with initialization
int b;                       // Declaration only (value is undefined!)
b = 20;                      // Assignment later

// Multiple variables of same type
int x = 1, y = 2, z = 3;

// Constants
const double PI = 3.14159;
const int MAX_SIZE = 100;

// Preprocessor constants (no type checking, simple text substitution)
#define BUFFER_SIZE 1024
#define VERSION "1.0"
```

### Variable Naming Rules

```c
// Valid variable names (snake_case is conventional in C)
int age = 25;
char first_name[] = "John";
double account_balance = 1000.50;
int is_valid = 1;

// Valid but less conventional
int _private_var = 10;
int number2 = 20;
int camelCase = 30;      // More common in other languages

// Invalid variable names
// int 2age = 25;         // Can't start with number
// int user-name = 5;     // Can't use hyphens
// int float = 5;         // Can't use reserved keywords
```

---

## Basic Operations

### Arithmetic Operators

```c
#include <stdio.h>

int main(void) {
    int a = 10;
    int b = 3;

    // Basic arithmetic
    int addition = a + b;           // 13
    int subtraction = a - b;        // 7
    int multiplication = a * b;     // 30
    int integer_division = a / b;   // 3 (integer division truncates)
    int modulus = a % b;            // 1 (remainder)

    // To get floating point division, cast one operand
    double division = (double)a / b;  // 3.333...

    printf("10 + 3 = %d\n", addition);
    printf("10 / 3 = %d (integer)\n", integer_division);
    printf("10 / 3 = %.2f (float)\n", division);
    printf("10 %% 3 = %d\n", modulus);  // %% to print literal %

    // Compound assignment operators
    int x = 5;
    x += 3;  // x = x + 3, now x = 8
    x -= 2;  // x = x - 2, now x = 6
    x *= 2;  // x = x * 2, now x = 12
    x /= 4;  // x = x / 4, now x = 3
    x %= 2;  // x = x % 2, now x = 1

    printf("Final x value: %d\n", x);

    // Increment and decrement
    int counter = 5;
    counter++;    // Post-increment, counter = 6
    ++counter;    // Pre-increment, counter = 7
    counter--;    // Post-decrement, counter = 6
    --counter;    // Pre-decrement, counter = 5

    // Difference between pre and post
    int val = 5;
    printf("Post-increment: %d\n", val++);  // Prints 5, then val becomes 6
    printf("After: %d\n", val);             // Prints 6
    printf("Pre-increment: %d\n", ++val);   // val becomes 7, then prints 7

    return 0;
}
```

### Comparison Operators

```c
#include <stdio.h>

int main(void) {
    int x = 5;
    int y = 10;

    // Comparison operations return 1 (true) or 0 (false)
    printf("5 == 10: %d\n", x == y);   // 0
    printf("5 != 10: %d\n", x != y);   // 1
    printf("5 < 10: %d\n", x < y);     // 1
    printf("5 > 10: %d\n", x > y);     // 0
    printf("5 <= 10: %d\n", x <= y);   // 1
    printf("5 >= 10: %d\n", x >= y);   // 0

    return 0;
}
```

### Logical Operators

```c
#include <stdio.h>

int main(void) {
    // Logical operators: &&, ||, !
    int a = 1;  // true
    int b = 0;  // false

    printf("1 && 0 = %d\n", a && b);   // 0 (false)
    printf("1 || 0 = %d\n", a || b);   // 1 (true)
    printf("!1 = %d\n", !a);           // 0 (false)

    // Short-circuit evaluation
    // In && : if left side is false, right side is not evaluated
    // In || : if left side is true, right side is not evaluated

    // Practical example
    int age = 20;
    int has_license = 1;
    int can_drive = (age >= 18) && has_license;

    printf("Can drive: %d\n", can_drive);

    return 0;
}
```

### Bitwise Operators

```c
#include <stdio.h>

int main(void) {
    unsigned int a = 0b1100;  // 12 in binary (C23, or use 12)
    unsigned int b = 0b1010;  // 10 in binary (C23, or use 10)

    printf("a & b  = %u\n", a & b);   // AND:  0b1000 = 8
    printf("a | b  = %u\n", a | b);   // OR:   0b1110 = 14
    printf("a ^ b  = %u\n", a ^ b);   // XOR:  0b0110 = 6
    printf("~a     = %u\n", ~a);      // NOT:  flips all bits
    printf("a << 1 = %u\n", a << 1);  // Left shift:  0b11000 = 24
    printf("a >> 1 = %u\n", a >> 1);  // Right shift: 0b0110 = 6

    // Common uses
    // Setting a bit
    unsigned int flags = 0;
    flags |= (1 << 3);   // Set bit 3

    // Clearing a bit
    flags &= ~(1 << 3);  // Clear bit 3

    // Checking a bit
    if (flags & (1 << 3)) {
        printf("Bit 3 is set\n");
    }

    return 0;
}
```

---

## Input and Output

### printf Format Specifiers

```c
#include <stdio.h>

int main(void) {
    // Common format specifiers
    printf("Character: %c\n", 'A');
    printf("String: %s\n", "Hello");
    printf("Integer: %d\n", 42);
    printf("Unsigned: %u\n", 42U);
    printf("Long: %ld\n", 100000L);
    printf("Float: %f\n", 3.14);
    printf("Double: %lf\n", 3.14);
    printf("Scientific: %e\n", 3.14);
    printf("Hex: %x\n", 255);         // ff
    printf("Hex (upper): %X\n", 255); // FF
    printf("Octal: %o\n", 255);       // 377
    printf("Pointer: %p\n", (void *)&main);
    printf("Percent: %%\n");

    // Width and precision
    printf("[%10d]\n", 42);       // Right-aligned, width 10
    printf("[%-10d]\n", 42);      // Left-aligned, width 10
    printf("[%010d]\n", 42);      // Zero-padded, width 10
    printf("[%.5f]\n", 3.14);     // 5 decimal places
    printf("[%8.2f]\n", 3.14);    // Width 8, 2 decimal places
    printf("[%.5s]\n", "Hello World");  // First 5 chars

    return 0;
}
```

### scanf for User Input

```c
#include <stdio.h>

int main(void) {
    // Reading an integer
    int age;
    printf("Enter your age: ");
    scanf("%d", &age);  // & is the address-of operator
    printf("You are %d years old\n", age);

    // Reading a float
    double height;
    printf("Enter your height: ");
    scanf("%lf", &height);
    printf("Height: %.2f\n", height);

    // Reading a single word (stops at whitespace)
    char name[50];
    printf("Enter your first name: ");
    scanf("%49s", name);  // No & needed for arrays; 49 limits input
    printf("Hello, %s!\n", name);

    // Reading a character
    char grade;
    printf("Enter a grade: ");
    scanf(" %c", &grade);  // Space before %c skips whitespace
    printf("Grade: %c\n", grade);

    // Reading multiple values
    int x, y;
    printf("Enter two numbers: ");
    scanf("%d %d", &x, &y);
    printf("Sum: %d\n", x + y);

    return 0;
}
```

### fgets for Safe String Input

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[100];

    // fgets reads an entire line (including spaces)
    printf("Enter a sentence: ");
    fgets(line, sizeof(line), stdin);

    // Remove trailing newline if present
    line[strcspn(line, "\n")] = '\0';

    printf("You said: '%s'\n", line);
    printf("Length: %zu\n", strlen(line));

    return 0;
}
```

### puts and putchar

```c
#include <stdio.h>

int main(void) {
    // puts - prints string with automatic newline
    puts("Hello, World!");  // Equivalent to printf("Hello, World!\n");

    // putchar - prints a single character
    putchar('H');
    putchar('i');
    putchar('\n');

    // getchar - reads a single character
    printf("Press a key: ");
    int ch = getchar();
    printf("You pressed: %c (ASCII %d)\n", ch, ch);

    return 0;
}
```

---

## Conditional Statements

### if, else if, else

```c
#include <stdio.h>

int main(void) {
    // Basic if statement
    int age = 18;

    if (age >= 18) {
        printf("You are an adult\n");
        printf("You can vote\n");
    }

    // if-else
    int temperature = 25;

    if (temperature > 30) {
        printf("It's hot outside\n");
    } else {
        printf("It's not too hot\n");
    }

    // if-else if-else
    int score = 85;
    char grade;

    if (score >= 90) {
        grade = 'A';
    } else if (score >= 80) {
        grade = 'B';
    } else if (score >= 70) {
        grade = 'C';
    } else if (score >= 60) {
        grade = 'D';
    } else {
        grade = 'F';
    }

    printf("Your grade is: %c\n", grade);

    return 0;
}
```

### switch Statements

```c
#include <stdio.h>

int main(void) {
    int day_number = 3;
    const char *day_name;

    switch (day_number) {
        case 1:
            day_name = "Monday";
            break;
        case 2:
            day_name = "Tuesday";
            break;
        case 3:
            day_name = "Wednesday";
            break;
        case 4:
            day_name = "Thursday";
            break;
        case 5:
            day_name = "Friday";
            break;
        case 6:
            day_name = "Saturday";
            break;
        case 7:
            day_name = "Sunday";
            break;
        default:
            day_name = "Invalid day";
            break;
    }

    printf("Day %d is %s\n", day_number, day_name);

    // Fall-through behavior (no break)
    int month = 3;
    const char *season;

    switch (month) {
        case 12:
        case 1:
        case 2:
            season = "Winter";
            break;
        case 3:
        case 4:
        case 5:
            season = "Spring";
            break;
        case 6:
        case 7:
        case 8:
            season = "Summer";
            break;
        case 9:
        case 10:
        case 11:
            season = "Fall";
            break;
        default:
            season = "Invalid month";
            break;
    }

    printf("Month %d is in %s\n", month, season);

    return 0;
}
```

### Ternary Operator

```c
#include <stdio.h>

int main(void) {
    int age = 20;

    // Ternary operator: condition ? value_if_true : value_if_false
    const char *status = (age >= 18) ? "Adult" : "Minor";
    printf("Status: %s\n", status);

    // Practical example
    int x = 10, y = 20;
    int max = (x > y) ? x : y;
    printf("Maximum of %d and %d is %d\n", x, y, max);

    // Absolute value
    int num = -5;
    int abs_val = (num >= 0) ? num : -num;
    printf("Absolute value of %d is %d\n", num, abs_val);

    return 0;
}
```

---

## Loops

### for Loops

```c
#include <stdio.h>

int main(void) {
    // Basic for loop
    printf("Counting to 5:\n");
    for (int i = 1; i <= 5; i++) {
        printf("Count: %d\n", i);
    }

    // Loop with different increment
    printf("\nEven numbers from 2 to 10:\n");
    for (int i = 2; i <= 10; i += 2) {
        printf("%d\n", i);
    }

    // Counting backwards
    printf("\nCountdown:\n");
    for (int i = 5; i >= 1; i--) {
        printf("%d\n", i);
    }
    printf("Blast off!\n");

    // Nested loops - multiplication table
    printf("\nMultiplication table (1-5):\n");
    for (int i = 1; i <= 5; i++) {
        for (int j = 1; j <= 5; j++) {
            printf("%4d", i * j);
        }
        printf("\n");
    }

    return 0;
}
```

### while and do-while Loops

```c
#include <stdio.h>

int main(void) {
    // Basic while loop
    int count = 0;
    while (count < 3) {
        printf("Count is: %d\n", count);
        count++;
    }

    // Summing numbers until sentinel value
    printf("\nEnter numbers to sum (0 to stop):\n");
    int sum = 0;
    int number;
    while (1) {
        printf("Enter number: ");
        scanf("%d", &number);
        if (number == 0) {
            break;
        }
        sum += number;
    }
    printf("Total sum: %d\n", sum);

    // do-while loop (executes at least once)
    int guess;
    int secret = 7;
    do {
        printf("Guess the number (1-10): ");
        scanf("%d", &guess);
        if (guess < secret) {
            printf("Too low!\n");
        } else if (guess > secret) {
            printf("Too high!\n");
        }
    } while (guess != secret);
    printf("Correct!\n");

    return 0;
}
```

### Loop Control

```c
#include <stdio.h>

int main(void) {
    // break: Exit loop immediately
    printf("Numbers with break:\n");
    for (int i = 0; i < 10; i++) {
        if (i == 5)
            break;
        printf("%d ", i);  // Prints 0 1 2 3 4
    }
    printf("\n");

    // continue: Skip rest of current iteration
    printf("\nSkip multiples of 3:\n");
    for (int i = 0; i < 10; i++) {
        if (i % 3 == 0)
            continue;
        printf("%d ", i);  // Prints 1 2 4 5 7 8
    }
    printf("\n");

    // Breaking out of nested loops with goto (C's labeled break)
    printf("\nSearching a 2D grid:\n");
    int grid[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int target = 5;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (grid[i][j] == target) {
                printf("Found %d at [%d][%d]\n", target, i, j);
                goto found;  // Break out of both loops
            }
        }
    }
    printf("Not found\n");
found:

    return 0;
}
```

---

## Functions

### Defining Functions

```c
#include <stdio.h>

// Function declarations (prototypes) - usually at the top or in a header
void say_hello(void);
void greet_person(const char *name);
int add_numbers(int a, int b);
double calculate_area(double length, double width);

// Function definitions
void say_hello(void) {
    printf("Hello from a function!\n");
}

void greet_person(const char *name) {
    printf("Hello, %s!\n", name);
}

int add_numbers(int a, int b) {
    return a + b;
}

double calculate_area(double length, double width) {
    return length * width;
}

int main(void) {
    say_hello();

    greet_person("Alice");
    greet_person("Bob");

    int sum = add_numbers(5, 3);
    printf("5 + 3 = %d\n", sum);

    double area = calculate_area(4.5, 6.2);
    printf("Area: %.2f\n", area);

    return 0;
}
```

### Pass by Value vs Pass by Pointer

```c
#include <stdio.h>

// Pass by value (makes a copy - original is unchanged)
void double_value(int x) {
    x *= 2;
    printf("Inside function: %d\n", x);
}

// Pass by pointer (modifies the original)
void double_value_ptr(int *x) {
    *x *= 2;
    printf("Inside function: %d\n", *x);
}

// Swapping two values (requires pointers)
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Returning multiple values via pointers
void min_max(const int *arr, int size, int *min, int *max) {
    *min = arr[0];
    *max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] < *min) *min = arr[i];
        if (arr[i] > *max) *max = arr[i];
    }
}

int main(void) {
    // Pass by value
    int val = 5;
    double_value(val);
    printf("After pass by value: %d\n\n", val);  // Still 5

    // Pass by pointer
    double_value_ptr(&val);
    printf("After pass by pointer: %d\n\n", val);  // Now 10

    // Swap
    int a = 10, b = 20;
    printf("Before swap: a=%d, b=%d\n", a, b);
    swap(&a, &b);
    printf("After swap: a=%d, b=%d\n\n", a, b);

    // Multiple return values
    int numbers[] = {3, 7, 1, 9, 4};
    int min, max;
    min_max(numbers, 5, &min, &max);
    printf("Min: %d, Max: %d\n", min, max);

    return 0;
}
```

### Recursion

```c
#include <stdio.h>

// Factorial
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Fibonacci
int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void) {
    printf("5! = %d\n", factorial(5));  // 120

    printf("Fibonacci sequence: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", fibonacci(i));
    }
    printf("\n");

    return 0;
}
```

---

## Arrays

### One-Dimensional Arrays

```c
#include <stdio.h>

int main(void) {
    // Declaring and initializing arrays
    int numbers[5];                           // Uninitialized array of 5 ints
    int primes[] = {2, 3, 5, 7, 11};         // Size inferred from initializer
    int zeros[10] = {0};                      // All elements initialized to 0
    int partial[5] = {1, 2};                  // {1, 2, 0, 0, 0}

    // Accessing array elements (0-indexed)
    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;
    numbers[3] = 40;
    numbers[4] = 50;

    printf("First prime: %d\n", primes[0]);
    printf("Array size: %zu\n", sizeof(primes) / sizeof(primes[0]));

    // Looping through arrays
    printf("Numbers: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // Common pattern: size macro
    #define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

    printf("Primes: ");
    for (size_t i = 0; i < ARRAY_SIZE(primes); i++) {
        printf("%d ", primes[i]);
    }
    printf("\n");

    return 0;
}
```

### Multi-Dimensional Arrays

```c
#include <stdio.h>

int main(void) {
    // 2D array (matrix)
    int matrix[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    printf("Matrix:\n");
    for (int row = 0; row < 2; row++) {
        for (int col = 0; col < 3; col++) {
            printf("%4d", matrix[row][col]);
        }
        printf("\n");
    }

    // 3x3 identity matrix
    int identity[3][3] = {
        {1, 0, 0},
        {0, 1, 0},
        {0, 0, 1}
    };

    printf("\nIdentity matrix:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%2d", identity[i][j]);
        }
        printf("\n");
    }

    return 0;
}
```

### Passing Arrays to Functions

```c
#include <stdio.h>

// Arrays decay to pointers when passed to functions
// You must pass the size separately
void print_array(const int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int sum_array(const int *arr, int size) {
    int total = 0;
    for (int i = 0; i < size; i++) {
        total += arr[i];
    }
    return total;
}

void reverse_array(int *arr, int size) {
    for (int i = 0; i < size / 2; i++) {
        int temp = arr[i];
        arr[i] = arr[size - 1 - i];
        arr[size - 1 - i] = temp;
    }
}

int main(void) {
    int numbers[] = {5, 3, 8, 1, 9, 2, 7};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("Original: ");
    print_array(numbers, size);

    printf("Sum: %d\n", sum_array(numbers, size));

    reverse_array(numbers, size);
    printf("Reversed: ");
    print_array(numbers, size);

    return 0;
}
```

---

## Pointers

### Pointer Basics

```c
#include <stdio.h>

int main(void) {
    int x = 42;
    int *ptr = &x;  // ptr stores the address of x

    printf("Value of x: %d\n", x);
    printf("Address of x: %p\n", (void *)&x);
    printf("Value of ptr: %p\n", (void *)ptr);    // Same address
    printf("Dereferenced ptr: %d\n", *ptr);         // 42

    // Modifying value through pointer
    *ptr = 100;
    printf("x after *ptr = 100: %d\n", x);  // 100

    // Pointer arithmetic
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;  // Points to first element

    printf("\nPointer arithmetic:\n");
    for (int i = 0; i < 5; i++) {
        printf("*(p + %d) = %d\n", i, *(p + i));
    }

    // Incrementing pointer
    p = arr;
    while (p < arr + 5) {
        printf("%d ", *p);
        p++;
    }
    printf("\n");

    return 0;
}
```

### Null Pointers and Void Pointers

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // NULL pointer - points to nothing
    int *ptr = NULL;

    // Always check for NULL before dereferencing
    if (ptr != NULL) {
        printf("Value: %d\n", *ptr);
    } else {
        printf("Pointer is NULL\n");
    }

    // void pointer - generic pointer (can point to any type)
    int num = 42;
    float fnum = 3.14f;

    void *generic = &num;
    printf("As int: %d\n", *(int *)generic);  // Must cast to dereference

    generic = &fnum;
    printf("As float: %.2f\n", *(float *)generic);

    return 0;
}
```

### Pointers and Arrays

```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};

    // Array name is a pointer to the first element
    printf("arr[0] = %d\n", arr[0]);
    printf("*arr   = %d\n", *arr);          // Same thing

    printf("arr[2] = %d\n", arr[2]);
    printf("*(arr+2) = %d\n", *(arr + 2));  // Same thing

    // Key difference: array names are not assignable
    // arr = some_other_pointer;  // ERROR: cannot assign to array

    // Pointer to pointer
    int x = 42;
    int *p = &x;
    int **pp = &p;

    printf("\nPointer to pointer:\n");
    printf("x = %d\n", x);
    printf("*p = %d\n", *p);
    printf("**pp = %d\n", **pp);

    return 0;
}
```

### Function Pointers

```c
#include <stdio.h>

// Functions to use with function pointers
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

// Function that takes a function pointer
int apply(int (*operation)(int, int), int a, int b) {
    return operation(a, b);
}

int main(void) {
    // Declare a function pointer
    int (*op)(int, int);

    op = add;
    printf("add(5, 3) = %d\n", op(5, 3));

    op = subtract;
    printf("subtract(5, 3) = %d\n", op(5, 3));

    // Using the apply function
    printf("apply(multiply, 5, 3) = %d\n", apply(multiply, 5, 3));

    // Array of function pointers
    int (*operations[])(int, int) = {add, subtract, multiply};
    const char *names[] = {"add", "subtract", "multiply"};

    for (int i = 0; i < 3; i++) {
        printf("%s(10, 4) = %d\n", names[i], operations[i](10, 4));
    }

    return 0;
}
```

---

## Strings

### String Basics

C has no built-in string type. Strings are arrays of `char` terminated by a null character (`'\0'`).

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    // String declaration
    char greeting[] = "Hello";              // Compiler adds '\0', size is 6
    char name[20] = "Alice";                // 20 chars allocated, rest are '\0'
    char manual[] = {'H', 'i', '\0'};       // Manual null termination

    // String literals are read-only
    const char *message = "Hello, World!";  // Points to string literal

    printf("Greeting: %s\n", greeting);
    printf("Length: %zu\n", strlen(greeting));  // 5 (doesn't count '\0')

    // Accessing characters
    printf("First char: %c\n", greeting[0]);
    printf("Last char: %c\n", greeting[strlen(greeting) - 1]);

    // Iterating over a string
    printf("Characters: ");
    for (int i = 0; greeting[i] != '\0'; i++) {
        printf("'%c' ", greeting[i]);
    }
    printf("\n");

    return 0;
}
```

### String Functions (string.h)

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char str1[50] = "Hello";
    char str2[] = "World";
    char buffer[100];

    // strlen - string length
    printf("Length of str1: %zu\n", strlen(str1));

    // strcpy - copy string
    strcpy(buffer, str1);
    printf("After strcpy: %s\n", buffer);

    // strncpy - copy with limit (safer)
    strncpy(buffer, str2, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination
    printf("After strncpy: %s\n", buffer);

    // strcat - concatenate strings
    strcpy(buffer, str1);
    strcat(buffer, ", ");
    strcat(buffer, str2);
    strcat(buffer, "!");
    printf("After strcat: %s\n", buffer);  // "Hello, World!"

    // strncat - concatenate with limit (safer)
    char safe[20] = "Hi";
    strncat(safe, " there!", sizeof(safe) - strlen(safe) - 1);
    printf("After strncat: %s\n", safe);

    // strcmp - compare strings (0 = equal)
    printf("strcmp(\"abc\", \"abc\"): %d\n", strcmp("abc", "abc"));  // 0
    printf("strcmp(\"abc\", \"def\"): %d\n", strcmp("abc", "def"));  // negative
    printf("strcmp(\"def\", \"abc\"): %d\n", strcmp("def", "abc"));  // positive

    // strncmp - compare first n characters
    printf("strncmp(\"Hello\", \"Help\", 3): %d\n", strncmp("Hello", "Help", 3));  // 0

    // strchr - find first occurrence of character
    const char *text = "Hello, World!";
    char *found = strchr(text, 'o');
    if (found) {
        printf("First 'o' at position: %ld\n", found - text);
    }

    // strstr - find substring
    found = strstr(text, "World");
    if (found) {
        printf("'World' found at position: %ld\n", found - text);
    }

    // strtok - split string by delimiter
    char csv[] = "apple,banana,cherry,date";
    char *token = strtok(csv, ",");
    printf("\nTokens:\n");
    while (token != NULL) {
        printf("- %s\n", token);
        token = strtok(NULL, ",");
    }

    return 0;
}
```

### String Conversion

```c
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main(void) {
    // String to number
    int num = atoi("42");
    long lnum = atol("1000000");
    double dnum = atof("3.14");

    printf("atoi: %d\n", num);
    printf("atol: %ld\n", lnum);
    printf("atof: %f\n", dnum);

    // Safer conversion with strtol
    const char *str = "123abc";
    char *end;
    long value = strtol(str, &end, 10);
    printf("strtol: %ld, remaining: '%s'\n", value, end);

    // Number to string with sprintf
    char buffer[50];
    sprintf(buffer, "The answer is %d", 42);
    printf("sprintf: %s\n", buffer);

    // snprintf (safer, with buffer size limit)
    snprintf(buffer, sizeof(buffer), "Pi is %.4f", 3.14159);
    printf("snprintf: %s\n", buffer);

    // Character classification (ctype.h)
    char ch = 'A';
    printf("\nCharacter '%c':\n", ch);
    printf("isalpha: %d\n", isalpha(ch));  // non-zero (true)
    printf("isdigit: %d\n", isdigit(ch));  // 0 (false)
    printf("isupper: %d\n", isupper(ch));  // non-zero
    printf("tolower: %c\n", tolower(ch));  // 'a'

    return 0;
}
```

---

## Structures

### Defining and Using Structs

```c
#include <stdio.h>
#include <string.h>

// Structure definition
struct Point {
    double x;
    double y;
};

// Structure with typedef (no need to write "struct" when using)
typedef struct {
    char name[50];
    int age;
    double gpa;
} Student;

int main(void) {
    // Declare and initialize a struct
    struct Point p1 = {3.0, 4.0};
    struct Point p2 = {.x = 1.0, .y = 2.0};  // Designated initializers (C99)

    printf("Point: (%.1f, %.1f)\n", p1.x, p1.y);

    // Modify struct members
    p1.x = 5.0;
    printf("Modified: (%.1f, %.1f)\n", p1.x, p1.y);

    // Using typedef struct
    Student s1 = {"Alice", 20, 3.85};
    Student s2;
    strcpy(s2.name, "Bob");
    s2.age = 22;
    s2.gpa = 3.5;

    printf("\nStudent: %s, Age: %d, GPA: %.2f\n", s1.name, s1.age, s1.gpa);
    printf("Student: %s, Age: %d, GPA: %.2f\n", s2.name, s2.age, s2.gpa);

    // Array of structs
    Student class[] = {
        {"Alice", 20, 3.85},
        {"Bob", 22, 3.50},
        {"Charlie", 21, 3.70}
    };

    printf("\nClass roster:\n");
    for (int i = 0; i < 3; i++) {
        printf("  %s (age %d): %.2f GPA\n",
               class[i].name, class[i].age, class[i].gpa);
    }

    return 0;
}
```

### Structs and Pointers

```c
#include <stdio.h>
#include <string.h>
#include <math.h>

typedef struct {
    double x;
    double y;
} Point;

// Pass struct by pointer (efficient, avoids copying)
void print_point(const Point *p) {
    printf("(%.1f, %.1f)\n", p->x, p->y);  // -> operator for pointer access
}

void move_point(Point *p, double dx, double dy) {
    p->x += dx;
    p->y += dy;
}

double distance(const Point *a, const Point *b) {
    double dx = a->x - b->x;
    double dy = a->y - b->y;
    return sqrt(dx * dx + dy * dy);
}

int main(void) {
    Point p1 = {0.0, 0.0};
    Point p2 = {3.0, 4.0};

    printf("p1 = ");
    print_point(&p1);

    move_point(&p1, 1.0, 2.0);
    printf("After move: ");
    print_point(&p1);

    printf("Distance: %.2f\n", distance(&p1, &p2));

    return 0;
}
```

### Nested Structs and Enums

```c
#include <stdio.h>

// Enum for categorization
typedef enum {
    RED,
    GREEN,
    BLUE,
    YELLOW
} Color;

// Nested struct
typedef struct {
    int x;
    int y;
} Position;

typedef struct {
    Position pos;
    Color color;
    int width;
    int height;
} Rectangle;

const char *color_name(Color c) {
    switch (c) {
        case RED:    return "Red";
        case GREEN:  return "Green";
        case BLUE:   return "Blue";
        case YELLOW: return "Yellow";
        default:     return "Unknown";
    }
}

int main(void) {
    Rectangle rect = {
        .pos = {10, 20},
        .color = BLUE,
        .width = 100,
        .height = 50
    };

    printf("Rectangle at (%d, %d), %dx%d, color: %s\n",
           rect.pos.x, rect.pos.y,
           rect.width, rect.height,
           color_name(rect.color));

    // Enum values are integers
    printf("RED = %d, GREEN = %d, BLUE = %d\n", RED, GREEN, BLUE);

    return 0;
}
```

---

## Memory Management

### malloc, calloc, realloc, free

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    // malloc - allocate uninitialized memory
    int *numbers = malloc(5 * sizeof(int));
    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize and use
    for (int i = 0; i < 5; i++) {
        numbers[i] = (i + 1) * 10;
    }

    printf("malloc'd array: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // calloc - allocate zero-initialized memory
    int *zeros = calloc(5, sizeof(int));
    if (zeros == NULL) {
        free(numbers);
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    printf("calloc'd array: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", zeros[i]);  // All zeros
    }
    printf("\n");

    // realloc - resize allocated memory
    numbers = realloc(numbers, 10 * sizeof(int));
    if (numbers == NULL) {
        free(zeros);
        fprintf(stderr, "Reallocation failed\n");
        return 1;
    }

    // Fill new elements
    for (int i = 5; i < 10; i++) {
        numbers[i] = (i + 1) * 10;
    }

    printf("realloc'd array: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // free - release allocated memory
    free(numbers);
    free(zeros);
    numbers = NULL;  // Good practice: set to NULL after freeing
    zeros = NULL;

    return 0;
}
```

### Dynamic Strings

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Duplicate a string (allocates memory)
char *string_duplicate(const char *src) {
    char *copy = malloc(strlen(src) + 1);
    if (copy != NULL) {
        strcpy(copy, src);
    }
    return copy;
}

// Concatenate two strings into new allocation
char *string_concat(const char *a, const char *b) {
    char *result = malloc(strlen(a) + strlen(b) + 1);
    if (result != NULL) {
        strcpy(result, a);
        strcat(result, b);
    }
    return result;
}

int main(void) {
    char *name = string_duplicate("Hello");
    char *full = string_concat(name, ", World!");

    printf("%s\n", full);  // "Hello, World!"

    free(name);
    free(full);

    return 0;
}
```

### Dynamic Arrays (Growable)

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} IntArray;

IntArray *array_create(int initial_capacity) {
    IntArray *arr = malloc(sizeof(IntArray));
    if (arr == NULL) return NULL;
    arr->data = malloc(initial_capacity * sizeof(int));
    if (arr->data == NULL) {
        free(arr);
        return NULL;
    }
    arr->size = 0;
    arr->capacity = initial_capacity;
    return arr;
}

int array_push(IntArray *arr, int value) {
    if (arr->size >= arr->capacity) {
        int new_cap = arr->capacity * 2;
        int *new_data = realloc(arr->data, new_cap * sizeof(int));
        if (new_data == NULL) return -1;
        arr->data = new_data;
        arr->capacity = new_cap;
    }
    arr->data[arr->size++] = value;
    return 0;
}

void array_print(const IntArray *arr) {
    printf("[");
    for (int i = 0; i < arr->size; i++) {
        printf("%d%s", arr->data[i], i < arr->size - 1 ? ", " : "");
    }
    printf("] (size=%d, cap=%d)\n", arr->size, arr->capacity);
}

void array_free(IntArray *arr) {
    free(arr->data);
    free(arr);
}

int main(void) {
    IntArray *arr = array_create(4);

    for (int i = 0; i < 10; i++) {
        array_push(arr, i * 10);
        array_print(arr);
    }

    array_free(arr);
    return 0;
}
```

---

## File Operations

### Reading and Writing Files

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char *filename = "example.txt";

    // Writing to a file
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file for writing");
        return 1;
    }

    fprintf(file, "Hello, World!\n");
    fprintf(file, "This is line 2.\n");
    fprintf(file, "This is line 3.\n");
    fputs("This is line 4.\n", file);
    fclose(file);
    printf("File written successfully\n");

    // Reading entire file line by line
    file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file for reading");
        return 1;
    }

    char line[256];
    int line_num = 1;
    printf("\nFile contents:\n");
    while (fgets(line, sizeof(line), file) != NULL) {
        printf("%d: %s", line_num++, line);
    }
    fclose(file);

    // Appending to a file
    file = fopen(filename, "a");
    if (file == NULL) {
        perror("Error opening file for appending");
        return 1;
    }

    fprintf(file, "This line was appended.\n");
    fclose(file);
    printf("\nText appended successfully\n");

    // Reading character by character
    file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    printf("\nCharacter count:\n");
    int ch;
    int char_count = 0;
    while ((ch = fgetc(file)) != EOF) {
        char_count++;
    }
    printf("Total characters: %d\n", char_count);
    fclose(file);

    // Delete the file
    remove(filename);
    printf("File deleted\n");

    return 0;
}
```

### Binary File Operations

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    int age;
    double score;
} Record;

int main(void) {
    const char *filename = "records.bin";

    // Write binary data
    Record records[] = {
        {"Alice", 20, 95.5},
        {"Bob", 22, 87.3},
        {"Charlie", 21, 91.0}
    };
    int count = sizeof(records) / sizeof(records[0]);

    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    fwrite(&count, sizeof(int), 1, file);
    fwrite(records, sizeof(Record), count, file);
    fclose(file);
    printf("Wrote %d records\n", count);

    // Read binary data
    file = fopen(filename, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    int read_count;
    fread(&read_count, sizeof(int), 1, file);

    Record *read_records = malloc(read_count * sizeof(Record));
    fread(read_records, sizeof(Record), read_count, file);
    fclose(file);

    printf("\nRead %d records:\n", read_count);
    for (int i = 0; i < read_count; i++) {
        printf("  %s, age %d, score %.1f\n",
               read_records[i].name,
               read_records[i].age,
               read_records[i].score);
    }

    free(read_records);
    remove(filename);

    return 0;
}
```

---

## Preprocessor and Header Files

### Preprocessor Directives

```c
#include <stdio.h>

// Object-like macros
#define PI 3.14159
#define MAX_SIZE 100
#define VERSION "1.0.0"

// Function-like macros
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))
#define ABS(x) ((x) >= 0 ? (x) : -(x))

// Conditional compilation
#define DEBUG 1

int main(void) {
    printf("Version: %s\n", VERSION);
    printf("PI: %f\n", PI);

    printf("MAX(3, 7) = %d\n", MAX(3, 7));
    printf("MIN(3, 7) = %d\n", MIN(3, 7));
    printf("SQUARE(5) = %d\n", SQUARE(5));
    printf("ABS(-3) = %d\n", ABS(-3));

    // Conditional compilation
    #if DEBUG
        printf("Debug mode is ON\n");
    #else
        printf("Release mode\n");
    #endif

    #ifdef MAX_SIZE
        printf("MAX_SIZE is defined as %d\n", MAX_SIZE);
    #endif

    #ifndef FEATURE_X
        printf("FEATURE_X is not defined\n");
    #endif

    return 0;
}
```

### Header Files

A header file (`*.h`) declares functions, types, and macros for use across multiple source files.

**mathutils.h:**
```c
#ifndef MATHUTILS_H
#define MATHUTILS_H

// Include guard prevents double inclusion

// Function declarations
double circle_area(double radius);
double circle_circumference(double radius);
int factorial(int n);
int is_prime(int n);

#endif // MATHUTILS_H
```

**mathutils.c:**
```c
#include "mathutils.h"
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

double circle_area(double radius) {
    return M_PI * radius * radius;
}

double circle_circumference(double radius) {
    return 2.0 * M_PI * radius;
}

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int is_prime(int n) {
    if (n < 2) return 0;
    if (n < 4) return 1;
    if (n % 2 == 0) return 0;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}
```

**main.c:**
```c
#include <stdio.h>
#include "mathutils.h"

int main(void) {
    double r = 5.0;
    printf("Circle (r=%.1f):\n", r);
    printf("  Area: %.2f\n", circle_area(r));
    printf("  Circumference: %.2f\n", circle_circumference(r));

    printf("5! = %d\n", factorial(5));
    printf("Is 17 prime? %s\n", is_prime(17) ? "Yes" : "No");

    return 0;
}
```

**Compiling multi-file programs:**
```bash
gcc -Wall -std=c11 main.c mathutils.c -o program -lm
./program
```

---

## Practice Exercises

### Exercise 1: Temperature Converter

```c
#include <stdio.h>

double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}

double fahrenheit_to_celsius(double fahrenheit) {
    return (fahrenheit - 32.0) * 5.0 / 9.0;
}

int main(void) {
    int choice;
    double temp;

    printf("Temperature Converter\n");
    printf("1. Celsius to Fahrenheit\n");
    printf("2. Fahrenheit to Celsius\n");
    printf("Choose option (1 or 2): ");
    scanf("%d", &choice);

    printf("Enter temperature: ");
    scanf("%lf", &temp);

    if (choice == 1) {
        printf("%.1f°C = %.1f°F\n", temp, celsius_to_fahrenheit(temp));
    } else if (choice == 2) {
        printf("%.1f°F = %.1f°C\n", temp, fahrenheit_to_celsius(temp));
    } else {
        printf("Invalid option\n");
    }

    return 0;
}
```

### Exercise 2: Simple Calculator

```c
#include <stdio.h>

int main(void) {
    double num1, num2;
    char operator;

    printf("Enter first number: ");
    scanf("%lf", &num1);

    printf("Enter operator (+, -, *, /): ");
    scanf(" %c", &operator);

    printf("Enter second number: ");
    scanf("%lf", &num2);

    double result;
    int valid = 1;

    switch (operator) {
        case '+': result = num1 + num2; break;
        case '-': result = num1 - num2; break;
        case '*': result = num1 * num2; break;
        case '/':
            if (num2 != 0) {
                result = num1 / num2;
            } else {
                printf("Error: Division by zero\n");
                return 1;
            }
            break;
        default:
            printf("Invalid operator\n");
            valid = 0;
    }

    if (valid) {
        printf("%.2f %c %.2f = %.2f\n", num1, operator, num2, result);
    }

    return 0;
}
```

### Exercise 3: Number Guessing Game

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    srand(time(NULL));
    int secret = (rand() % 100) + 1;
    int attempts = 0;
    int max_attempts = 7;
    int guess;

    printf("I'm thinking of a number between 1 and 100.\n");
    printf("You have %d attempts.\n", max_attempts);

    while (attempts < max_attempts) {
        printf("Enter your guess: ");
        scanf("%d", &guess);
        attempts++;

        if (guess == secret) {
            printf("Congratulations! You guessed it in %d attempts!\n", attempts);
            return 0;
        } else if (guess < secret) {
            printf("Too low! %d attempts remaining.\n", max_attempts - attempts);
        } else {
            printf("Too high! %d attempts remaining.\n", max_attempts - attempts);
        }
    }

    printf("Game over! The number was %d\n", secret);

    return 0;
}
```

### Exercise 4: Linked List

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

// Create a new node
Node *node_create(int data) {
    Node *node = malloc(sizeof(Node));
    if (node != NULL) {
        node->data = data;
        node->next = NULL;
    }
    return node;
}

// Push to front of list
void list_push(Node **head, int data) {
    Node *new_node = node_create(data);
    new_node->next = *head;
    *head = new_node;
}

// Append to end of list
void list_append(Node **head, int data) {
    Node *new_node = node_create(data);
    if (*head == NULL) {
        *head = new_node;
        return;
    }
    Node *current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

// Print the list
void list_print(const Node *head) {
    const Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

// Get length
int list_length(const Node *head) {
    int count = 0;
    while (head != NULL) {
        count++;
        head = head->next;
    }
    return count;
}

// Free entire list
void list_free(Node **head) {
    Node *current = *head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    *head = NULL;
}

int main(void) {
    Node *list = NULL;

    list_append(&list, 10);
    list_append(&list, 20);
    list_append(&list, 30);
    list_push(&list, 5);

    printf("List: ");
    list_print(list);
    printf("Length: %d\n", list_length(list));

    list_free(&list);
    printf("After free: ");
    list_print(list);

    return 0;
}
```
