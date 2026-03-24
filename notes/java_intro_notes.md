# Elementary Java Programming Concepts

## Table of Contents

1. [Getting Started with Java](#getting-started-with-java)
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

## Getting Started with Java

### What is Java?

Java is a widely-used, object-oriented programming language developed by Sun Microsystems (now owned by Oracle). Key features:
- **Strongly typed**: Variables must be declared with specific types
- **Object-oriented**: Everything is based on classes and objects
- **Platform independent**: "Write once, run anywhere" via the Java Virtual Machine (JVM)
- **Memory managed**: Automatic garbage collection
- **Versatile**: Used for web backends, Android apps, enterprise software, and more

### Your First Java Program

```java
public class HelloWorld {
    public static void main(String[] args) {
        // This is a comment
        System.out.println("Hello, World!");
    }
}
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **public class HelloWorld** - Defines a class (file name must match class name: `HelloWorld.java`)
- **public static void main(String[] args)** - Entry point of the program
- **System.out.println()** - Prints text to console with a newline
- **System.out.print()** - Prints text without a newline
- **//** - Single-line comment
- **/* ... */** - Multi-line comment

### Development Environment

- **IntelliJ IDEA**: Full-featured IDE (recommended for beginners)
- **Eclipse**: Popular open-source IDE
- **Visual Studio Code**: Lightweight editor with Java extensions
- **JDK (Java Development Kit)**: Required to compile and run Java programs

### Compiling and Running

```bash
javac HelloWorld.java    # Compile to bytecode
java HelloWorld          # Run the compiled class
```

---

## Variables and Data Types

### Variable Declaration

In Java, you must declare variables with their type before using them.

```java
public class Variables {
    public static void main(String[] args) {
        // Declaring variables
        String name = "Alice";
        int age = 25;
        double height = 5.6;
        boolean isStudent = true;

        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Height: " + height);
        System.out.println("Is Student: " + isStudent);
    }
}
```

### Primitive Data Types

#### 1. Integer Types
```java
// Different integer types
byte smallNumber = 127;           // -128 to 127
short shortNumber = 32000;        // -32,768 to 32,767
int number = 2000000;             // -2.1 billion to 2.1 billion
long bigNumber = 9000000000L;     // Very large integers

System.out.println("int: " + number);
```

#### 2. Floating Point Types
```java
// Decimal numbers
float precision = 3.14f;          // 7 digits precision
double price = 19.99;             // 15-17 digits precision

System.out.println("float: " + precision);
System.out.println("double: " + price);
```

#### 3. Character and Boolean Types
```java
// Character (single character, uses single quotes)
char grade = 'A';
char unicodeChar = '\u0041';      // Also 'A'

// Boolean
boolean isRaining = false;
boolean isSunny = true;

System.out.println("Grade: " + grade);
System.out.println("Is raining: " + isRaining);
```

#### 4. String Type (Reference Type)
```java
// Strings are objects, not primitives
String firstName = "John";
String lastName = "Doe";

System.out.println("Full name: " + firstName + " " + lastName);
```

### Variable Initialization

```java
// Different ways to declare and initialize
int a = 10;                       // Declaration with initialization
int b;                            // Declaration only
b = 20;                           // Assignment later

// Multiple variables of same type
int x = 1, y = 2, z = 3;

// Type inference with 'var' keyword (Java 10+)
var name = "Alice";               // Compiler infers String
var count = 42;                   // Compiler infers int
var price = 19.99;                // Compiler infers double

// Constants (cannot be changed)
final double PI = 3.14159;
final String COMPANY_NAME = "TechCorp";
```

### Variable Naming Rules

```java
// Valid variable names (camelCase convention)
int age = 25;
String firstName = "John";
double accountBalance = 1000.50;
boolean isUserLoggedIn = true;

// Valid but not conventional
int _privateVar = 10;
int $dollarVar = 20;
int number2 = 30;

// Invalid variable names (these cause compilation errors)
// int 2age = 25;           // Can't start with number
// int user-name = "Bob";   // Can't use hyphens
// int class = 5;           // Can't use reserved keywords
```

---

## Basic Operations

### Arithmetic Operators

```java
public class Arithmetic {
    public static void main(String[] args) {
        int a = 10;
        int b = 3;

        // Basic arithmetic
        int addition = a + b;                // 13
        int subtraction = a - b;             // 7
        int multiplication = a * b;          // 30
        double division = (double) a / b;    // 3.333... (cast to double)
        int integerDivision = a / b;         // 3 (integer division)
        int modulus = a % b;                 // 1 (remainder)

        System.out.println("10 + 3 = " + addition);
        System.out.printf("10 / 3 = %.2f%n", division);
        System.out.println("10 % 3 = " + modulus);

        // Compound assignment operators
        int x = 5;
        x += 3;  // x = x + 3, now x = 8
        x -= 2;  // x = x - 2, now x = 6
        x *= 2;  // x = x * 2, now x = 12
        x /= 4;  // x = x / 4, now x = 3

        System.out.println("Final x value: " + x);

        // Increment and decrement
        int counter = 5;
        counter++;    // Post-increment, counter = 6
        ++counter;    // Pre-increment, counter = 7
        counter--;    // Post-decrement, counter = 6
        --counter;    // Pre-decrement, counter = 5

        System.out.println("Counter: " + counter);
    }
}
```

### Comparison Operators

```java
public class Comparison {
    public static void main(String[] args) {
        int x = 5;
        int y = 10;

        // Comparison operations return boolean
        boolean equal = x == y;            // false
        boolean notEqual = x != y;         // true
        boolean lessThan = x < y;          // true
        boolean greaterThan = x > y;       // false
        boolean lessEqual = x <= y;        // true
        boolean greaterEqual = x >= y;     // false

        System.out.println("5 == 10: " + equal);
        System.out.println("5 < 10: " + lessThan);
        System.out.println("5 != 10: " + notEqual);
    }
}
```

### Logical Operators

```java
public class Logical {
    public static void main(String[] args) {
        // Logical operators: &&, ||, !
        boolean a = true;
        boolean b = false;

        boolean andResult = a && b;    // false (both must be true)
        boolean orResult = a || b;     // true (at least one must be true)
        boolean notResult = !a;        // false (opposite of a)

        System.out.println("true && false = " + andResult);
        System.out.println("true || false = " + orResult);
        System.out.println("!true = " + notResult);

        // Practical example
        int age = 20;
        boolean hasLicense = true;
        boolean canDrive = age >= 18 && hasLicense;

        System.out.println("Can drive: " + canDrive);
    }
}
```

---

## Input and Output

### Getting User Input

```java
import java.util.Scanner;

public class UserInput {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Reading string input
        System.out.print("What's your name? ");
        String name = scanner.nextLine();
        System.out.println("Hello, " + name + "!");

        // Reading numeric input
        System.out.print("How old are you? ");
        int age = scanner.nextInt();
        scanner.nextLine(); // Consume leftover newline

        System.out.print("What's your height in meters? ");
        double height = scanner.nextDouble();

        System.out.println("You are " + age + " years old and " + height + "m tall");

        // Reading different types
        System.out.print("Enter a word: ");
        scanner.nextLine(); // Consume leftover newline
        String word = scanner.next();        // Reads single word
        System.out.println("You entered: " + word);

        scanner.close(); // Always close the scanner
    }
}
```

### Formatting Output

```java
public class FormattedOutput {
    public static void main(String[] args) {
        String name = "Alice";
        int age = 25;
        double gpa = 3.85;

        // String concatenation
        System.out.println("Hello " + name);

        // printf formatting (like C)
        System.out.printf("Hello %s, you are %d years old%n", name, age);
        System.out.printf("Your GPA is %.2f%n", gpa);

        // Common format specifiers
        double money = 1234.56;

        System.out.printf("String: %s%n", name);
        System.out.printf("Integer: %d%n", age);
        System.out.printf("Float: %.2f%n", gpa);
        System.out.printf("Currency: $%,.2f%n", money);
        System.out.printf("Padded: %10d%n", age);       // Right-aligned in 10 chars
        System.out.printf("Padded: %-10d|%n", age);     // Left-aligned in 10 chars

        // String.format (returns a string instead of printing)
        String formatted = String.format("Name: %s, Age: %d", name, age);
        System.out.println(formatted);
    }
}
```

---

## Conditional Statements

### if, else if, else

```java
public class Conditionals {
    public static void main(String[] args) {
        // Basic if statement
        int age = 18;

        if (age >= 18) {
            System.out.println("You are an adult");
            System.out.println("You can vote");
        }

        // if-else
        int temperature = 25;

        if (temperature > 30) {
            System.out.println("It's hot outside");
        } else {
            System.out.println("It's not too hot");
        }

        // if-else if-else
        int score = 85;
        String grade;

        if (score >= 90) {
            grade = "A";
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else if (score >= 60) {
            grade = "D";
        } else {
            grade = "F";
        }

        System.out.println("Your grade is: " + grade);
    }
}
```

### switch Statements

```java
public class SwitchExample {
    public static void main(String[] args) {
        // Traditional switch statement
        int dayNumber = 3;
        String dayName;

        switch (dayNumber) {
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

        System.out.println("Day " + dayNumber + " is " + dayName);

        // Enhanced switch expression (Java 14+)
        String season = switch (6) {
            case 12, 1, 2 -> "Winter";
            case 3, 4, 5 -> "Spring";
            case 6, 7, 8 -> "Summer";
            case 9, 10, 11 -> "Fall";
            default -> "Invalid month";
        };

        System.out.println("Month 6 is in " + season);

        // Switch with strings
        String command = "start";
        switch (command) {
            case "start":
                System.out.println("Starting...");
                break;
            case "stop":
                System.out.println("Stopping...");
                break;
            default:
                System.out.println("Unknown command");
        }
    }
}
```

### Ternary Operator

```java
public class Ternary {
    public static void main(String[] args) {
        int age = 20;

        // Ternary operator: condition ? value_if_true : value_if_false
        String status = age >= 18 ? "Adult" : "Minor";
        System.out.println("Status: " + status);

        // Nested ternary (use sparingly)
        int score = 85;
        String grade = score >= 90 ? "A" : score >= 80 ? "B" : "C or below";
        System.out.println("Grade: " + grade);

        // Practical example
        int x = 10, y = 20;
        int max = x > y ? x : y;
        System.out.println("Maximum of " + x + " and " + y + " is " + max);
    }
}
```

---

## Loops

### for Loops

```java
public class ForLoops {
    public static void main(String[] args) {
        // Basic for loop
        System.out.println("Counting to 5:");
        for (int i = 1; i <= 5; i++) {
            System.out.println("Count: " + i);
        }

        // Loop with different increment
        System.out.println("\nEven numbers from 2 to 10:");
        for (int i = 2; i <= 10; i += 2) {
            System.out.println(i);
        }

        // Counting backwards
        System.out.println("\nCountdown:");
        for (int i = 5; i >= 1; i--) {
            System.out.println(i);
        }
        System.out.println("Blast off!");

        // Loop through array
        String[] fruits = {"apple", "banana", "cherry"};
        System.out.println("\nFruits:");
        for (int i = 0; i < fruits.length; i++) {
            System.out.println((i + 1) + ". " + fruits[i]);
        }
    }
}
```

### Enhanced for (for-each) Loops

```java
public class ForEachLoops {
    public static void main(String[] args) {
        // for-each loop for arrays
        String[] colors = {"red", "green", "blue", "yellow"};

        System.out.println("Colors:");
        for (String color : colors) {
            System.out.println("- " + color);
        }

        // for-each with different data types
        int[] numbers = {1, 2, 3, 4, 5};
        int sum = 0;

        for (int number : numbers) {
            sum += number;
        }

        System.out.println("Sum of numbers: " + sum);

        // for-each with string (each character)
        String word = "Hello";
        System.out.println("Letters in '" + word + "':");
        for (char letter : word.toCharArray()) {
            System.out.println(letter);
        }
    }
}
```

### while and do-while Loops

```java
import java.util.Scanner;

public class WhileLoops {
    public static void main(String[] args) {
        // Basic while loop
        int count = 0;
        while (count < 3) {
            System.out.println("Count is: " + count);
            count++;
        }

        // Input validation with while
        Scanner scanner = new Scanner(System.in);
        int number;
        while (true) {
            System.out.print("Enter a number between 1 and 10: ");
            if (scanner.hasNextInt()) {
                number = scanner.nextInt();
                if (number >= 1 && number <= 10) {
                    System.out.println("Valid number: " + number);
                    break;
                }
            } else {
                scanner.next(); // Discard invalid input
            }
            System.out.println("Invalid input. Try again.");
        }

        // do-while loop (executes at least once)
        String input;
        do {
            System.out.print("Enter 'quit' to exit: ");
            input = scanner.next();
            System.out.println("You entered: " + input);
        } while (!input.equalsIgnoreCase("quit"));

        System.out.println("Goodbye!");
        scanner.close();
    }
}
```

### Loop Control

```java
public class LoopControl {
    public static void main(String[] args) {
        // break: Exit loop immediately
        System.out.println("Numbers with break:");
        for (int i = 0; i < 10; i++) {
            if (i == 5)
                break;
            System.out.println(i); // Prints 0, 1, 2, 3, 4
        }

        // continue: Skip rest of current iteration
        System.out.println("\nNumbers with continue (skip 3):");
        for (int i = 0; i < 6; i++) {
            if (i == 3)
                continue;
            System.out.println(i); // Prints 0, 1, 2, 4, 5
        }

        // Labeled break (breaks out of outer loop)
        System.out.println("\nLabeled break:");
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (i == 1 && j == 1)
                    break outer; // Breaks both loops
                System.out.println("i=" + i + ", j=" + j);
            }
        }
    }
}
```

---

## Methods

### Defining Methods

```java
public class Methods {

    // Method with no parameters and no return value
    static void sayHello() {
        System.out.println("Hello from a method!");
    }

    // Method with parameters
    static void greetPerson(String name) {
        System.out.println("Hello, " + name + "!");
    }

    // Method with return value
    static int addNumbers(int a, int b) {
        int result = a + b;
        return result;
    }

    // Method with multiple parameters and return value
    static double calculateArea(double length, double width) {
        return length * width;
    }

    public static void main(String[] args) {
        // Calling methods
        sayHello();

        greetPerson("Alice");
        greetPerson("Bob");

        int sum = addNumbers(5, 3);
        System.out.println("5 + 3 = " + sum);

        double area = calculateArea(4.5, 6.2);
        System.out.printf("Area: %.2f%n", area);
    }
}
```

### Method Overloading

```java
public class Overloading {

    // Method overloading - same name, different parameters
    static int add(int a, int b) {
        return a + b;
    }

    static double add(double a, double b) {
        return a + b;
    }

    static int add(int a, int b, int c) {
        return a + b + c;
    }

    static String add(String a, String b) {
        return a + b;
    }

    public static void main(String[] args) {
        System.out.println(add(5, 3));              // Calls int version
        System.out.println(add(5.5, 3.2));          // Calls double version
        System.out.println(add(1, 2, 3));           // Calls three-parameter version
        System.out.println(add("Hello", " World")); // Calls String version
    }
}
```

### Varargs and Method Features

```java
public class MethodFeatures {

    // Varargs (variable number of arguments)
    static int sumAll(int... numbers) {
        int total = 0;
        for (int num : numbers) {
            total += num;
        }
        return total;
    }

    // Returning multiple values via array
    static int[] getMinMax(int[] numbers) {
        int min = numbers[0];
        int max = numbers[0];
        for (int num : numbers) {
            if (num < min) min = num;
            if (num > max) max = num;
        }
        return new int[]{min, max};
    }

    // Recursive method
    static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        // Varargs
        System.out.println("Sum: " + sumAll(1, 2, 3));         // 6
        System.out.println("Sum: " + sumAll(1, 2, 3, 4, 5));   // 15

        // Multiple return values
        int[] values = {3, 7, 1, 9, 4};
        int[] minMax = getMinMax(values);
        System.out.println("Min: " + minMax[0] + ", Max: " + minMax[1]);

        // Recursion
        System.out.println("5! = " + factorial(5));  // 120
    }
}
```

---

## Arrays and Collections

### Arrays

```java
public class Arrays {
    public static void main(String[] args) {
        // Declaring and initializing arrays
        int[] numbers = new int[5];                           // Array of 5 integers
        String[] fruits = {"apple", "banana", "cherry"};      // Initialize with values

        // Accessing array elements (0-indexed)
        numbers[0] = 10;
        numbers[1] = 20;
        numbers[2] = 30;

        System.out.println("First fruit: " + fruits[0]);
        System.out.println("Array length: " + fruits.length);

        // Looping through arrays
        System.out.println("Numbers:");
        for (int i = 0; i < numbers.length; i++) {
            System.out.println("numbers[" + i + "] = " + numbers[i]);
        }

        System.out.println("Fruits:");
        for (String fruit : fruits) {
            System.out.println("- " + fruit);
        }

        // Multi-dimensional arrays
        int[][] matrix = {{1, 2, 3}, {4, 5, 6}};

        System.out.println("Matrix:");
        for (int row = 0; row < matrix.length; row++) {
            for (int col = 0; col < matrix[row].length; col++) {
                System.out.print(matrix[row][col] + " ");
            }
            System.out.println();
        }

        // Useful array operations (java.util.Arrays)
        int[] nums = {5, 2, 8, 1, 9};
        java.util.Arrays.sort(nums);
        System.out.println("Sorted: " + java.util.Arrays.toString(nums));

        int index = java.util.Arrays.binarySearch(nums, 5);
        System.out.println("Index of 5: " + index);
    }
}
```

### ArrayList

```java
import java.util.ArrayList;
import java.util.Collections;

public class ArrayListExample {
    public static void main(String[] args) {
        // Creating lists (dynamic arrays)
        ArrayList<String> names = new ArrayList<>();
        ArrayList<Integer> numbers = new ArrayList<>(java.util.Arrays.asList(1, 2, 3, 4, 5));

        // Adding elements
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");

        // Inserting at specific position
        names.add(1, "David");  // Insert at index 1

        // Accessing elements
        System.out.println("First name: " + names.get(0));
        System.out.println("List size: " + names.size());

        // Removing elements
        names.remove("Bob");            // Remove by value
        names.remove(0);                // Remove by index

        // Checking if element exists
        if (names.contains("Charlie")) {
            System.out.println("Charlie is in the list");
        }

        // Looping through list
        System.out.println("Names in list:");
        for (String name : names) {
            System.out.println("- " + name);
        }

        // List methods
        Collections.sort(numbers);          // Sort ascending
        Collections.reverse(numbers);       // Reverse the order

        System.out.println("Sorted numbers (descending):");
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();

        // Finding elements
        int index = numbers.indexOf(3);
        System.out.println("Index of 3: " + index);

        // Converting to array
        String[] nameArray = names.toArray(new String[0]);
        System.out.println("Converted to array, length: " + nameArray.length);
    }
}
```

### HashMap

```java
import java.util.HashMap;
import java.util.Map;

public class HashMapExample {
    public static void main(String[] args) {
        // Creating maps (key-value pairs)
        HashMap<String, Integer> ages = new HashMap<>();
        HashMap<String, String> capitals = new HashMap<>(Map.of(
            "USA", "Washington D.C.",
            "France", "Paris",
            "Japan", "Tokyo"
        ));

        // Adding key-value pairs
        ages.put("Alice", 25);
        ages.put("Bob", 30);
        ages.put("Charlie", 35);

        // Accessing values
        System.out.println("Alice's age: " + ages.get("Alice"));
        System.out.println("Capital of France: " + capitals.get("France"));

        // Checking if key exists
        if (ages.containsKey("Bob")) {
            System.out.println("Bob's age: " + ages.get("Bob"));
        }

        // Safe access with getOrDefault
        int davidAge = ages.getOrDefault("David", -1);
        if (davidAge == -1) {
            System.out.println("David not found in map");
        }

        // Modifying values
        ages.put("Alice", 26);  // Update existing

        // Removing key-value pairs
        ages.remove("Charlie");

        // Looping through map
        System.out.println("\nAll ages:");
        for (Map.Entry<String, Integer> entry : ages.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }

        // Alternative loop syntax
        System.out.println("\nAll capitals:");
        capitals.forEach((country, capital) ->
            System.out.println(country + " -> " + capital)
        );

        // Getting all keys or values
        System.out.println("\nKeys: " + ages.keySet());
        System.out.println("Values: " + ages.values());
    }
}
```

---

## String Manipulation

### String Basics

```java
public class StringBasics {
    public static void main(String[] args) {
        String text = "Hello, World!";

        // String properties and methods
        System.out.println("Length: " + text.length());
        System.out.println("Uppercase: " + text.toUpperCase());
        System.out.println("Lowercase: " + text.toLowerCase());

        // String checking methods
        System.out.println("Starts with 'Hello': " + text.startsWith("Hello"));
        System.out.println("Ends with '!': " + text.endsWith("!"));
        System.out.println("Contains 'World': " + text.contains("World"));
        System.out.println("Is empty: " + text.isEmpty());
        System.out.println("Is blank: " + text.isBlank());  // Java 11+

        // String indexing
        System.out.println("First character: " + text.charAt(0));
        System.out.println("Last character: " + text.charAt(text.length() - 1));

        // Finding substrings
        int index = text.indexOf("World");
        System.out.println("'World' found at index: " + index);

        int lastIndex = text.lastIndexOf("l");
        System.out.println("Last 'l' at index: " + lastIndex);
    }
}
```

### String Manipulation

```java
public class StringManipulation {
    public static void main(String[] args) {
        String sentence = "  The quick brown fox jumps over the lazy dog  ";

        // Trimming whitespace
        System.out.println("Original: '" + sentence + "'");
        System.out.println("Trimmed: '" + sentence.trim() + "'");
        System.out.println("Strip: '" + sentence.strip() + "'");  // Java 11+

        // Substring
        String text = "Hello, World!";
        System.out.println("Substring(0,5): " + text.substring(0, 5));   // "Hello"
        System.out.println("Substring(7): " + text.substring(7));         // "World!"

        // Replacing
        System.out.println("Replace: " + text.replace("World", "Java"));
        System.out.println("Replace all vowels: " + text.replaceAll("[aeiou]", "*"));

        // Splitting
        String csv = "apple,banana,cherry,date";
        String[] parts = csv.split(",");
        System.out.println("Split CSV:");
        for (String part : parts) {
            System.out.println("- " + part);
        }

        // Joining
        String joined = String.join(" | ", parts);
        System.out.println("Joined: " + joined);

        // String comparison (NEVER use == for strings)
        String a = "hello";
        String b = "Hello";
        System.out.println("equals: " + a.equals(b));                // false
        System.out.println("equalsIgnoreCase: " + a.equalsIgnoreCase(b)); // true
        System.out.println("compareTo: " + a.compareTo(b));          // positive number

        // StringBuilder for efficient concatenation
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) {
            sb.append("Item ").append(i).append(", ");
        }
        String result = sb.toString();
        System.out.println("Built string: " + result);
    }
}
```

---

## Error Handling

### Try-Catch

```java
import java.util.InputMismatchException;
import java.util.Scanner;

public class ErrorHandling {
    public static void main(String[] args) {
        // Basic try-catch
        try {
            int result = 10 / 0;
            System.out.println(result);
        } catch (ArithmeticException e) {
            System.out.println("Error: Cannot divide by zero");
            System.out.println("Message: " + e.getMessage());
        }

        // Multiple catch blocks
        try {
            int[] numbers = {1, 2, 3};
            System.out.println(numbers[10]); // ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Error: Index out of bounds");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }

        // try-catch-finally
        Scanner scanner = null;
        try {
            scanner = new Scanner(System.in);
            System.out.print("Enter a number: ");
            int number = scanner.nextInt();
            System.out.println("You entered: " + number);
        } catch (InputMismatchException e) {
            System.out.println("Error: Please enter a valid number");
        } finally {
            // Always executes, even if exception occurs
            System.out.println("This always runs");
        }

        // try-with-resources (auto-closes resources)
        try (Scanner sc = new Scanner(System.in)) {
            System.out.print("Enter text: ");
            String input = sc.nextLine();
            System.out.println("You said: " + input);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

### Throwing Exceptions

```java
public class ThrowingExceptions {

    // Method that throws an exception
    static double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }

    // Method with checked exception (must declare with throws)
    static int parseAge(String input) throws NumberFormatException {
        int age = Integer.parseInt(input);
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Age must be between 0 and 150");
        }
        return age;
    }

    public static void main(String[] args) {
        // Handling thrown exceptions
        try {
            double result = divide(10, 0);
        } catch (IllegalArgumentException e) {
            System.out.println("Caught: " + e.getMessage());
        }

        // Handling checked exceptions
        try {
            int age = parseAge("abc");
        } catch (NumberFormatException e) {
            System.out.println("Invalid number format");
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid age: " + e.getMessage());
        }
    }
}
```

---

## File Operations

### Reading and Writing Files

```java
import java.io.*;
import java.nio.file.*;
import java.util.List;

public class FileOperations {
    public static void main(String[] args) {
        String fileName = "example.txt";

        // Writing to a file (modern approach with Files)
        try {
            Files.writeString(Path.of(fileName), "Hello, World!\nThis is line 2.\nThis is line 3.\n");
            System.out.println("File written successfully");
        } catch (IOException e) {
            System.out.println("Error writing file: " + e.getMessage());
        }

        // Reading entire file as string
        try {
            String content = Files.readString(Path.of(fileName));
            System.out.println("File content:\n" + content);
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

        // Reading file line by line
        try {
            List<String> lines = Files.readAllLines(Path.of(fileName));
            System.out.println("Lines:");
            for (int i = 0; i < lines.size(); i++) {
                System.out.println((i + 1) + ": " + lines.get(i));
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

        // Appending to a file
        try {
            Files.writeString(Path.of(fileName), "This is appended.\n",
                StandardOpenOption.APPEND);
            System.out.println("Text appended successfully");
        } catch (IOException e) {
            System.out.println("Error appending: " + e.getMessage());
        }

        // Checking if file exists
        Path path = Path.of(fileName);
        System.out.println("File exists: " + Files.exists(path));
        System.out.println("Is directory: " + Files.isDirectory(path));

        // Deleting a file
        try {
            Files.deleteIfExists(path);
            System.out.println("File deleted");
        } catch (IOException e) {
            System.out.println("Error deleting file: " + e.getMessage());
        }
    }
}
```

### BufferedReader and BufferedWriter

```java
import java.io.*;

public class BufferedIO {
    public static void main(String[] args) {
        String fileName = "buffered_example.txt";

        // Writing with BufferedWriter
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            writer.write("Line 1");
            writer.newLine();
            writer.write("Line 2");
            writer.newLine();
            writer.write("Line 3");
            System.out.println("Written with BufferedWriter");
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // Reading with BufferedReader
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // Cleanup
        new File(fileName).delete();
    }
}
```

---

## Classes and Objects

### Basic Class

```java
public class Dog {
    // Instance variables (fields)
    String name;
    String breed;
    int age;

    // Constructor
    public Dog(String name, String breed, int age) {
        this.name = name;
        this.breed = breed;
        this.age = age;
    }

    // Default constructor
    public Dog() {
        this.name = "Unknown";
        this.breed = "Mixed";
        this.age = 0;
    }

    // Methods
    public void bark() {
        System.out.println(name + " says: Woof!");
    }

    public void describe() {
        System.out.println(name + " is a " + age + "-year-old " + breed);
    }

    public int getAgeInHumanYears() {
        return age * 7;
    }

    // toString method
    @Override
    public String toString() {
        return "Dog{name='" + name + "', breed='" + breed + "', age=" + age + "}";
    }

    public static void main(String[] args) {
        // Creating objects
        Dog dog1 = new Dog("Buddy", "Golden Retriever", 3);
        Dog dog2 = new Dog("Max", "German Shepherd", 5);
        Dog dog3 = new Dog(); // Uses default constructor

        // Using objects
        dog1.bark();
        dog2.describe();
        System.out.println(dog1.name + " in human years: " + dog1.getAgeInHumanYears());
        System.out.println(dog3); // Calls toString()
    }
}
```

### Encapsulation (Getters and Setters)

```java
public class BankAccount {
    // Private fields (encapsulation)
    private String owner;
    private double balance;

    // Constructor
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        if (initialBalance >= 0) {
            this.balance = initialBalance;
        } else {
            this.balance = 0;
            System.out.println("Initial balance cannot be negative. Set to 0.");
        }
    }

    // Getter methods
    public String getOwner() {
        return owner;
    }

    public double getBalance() {
        return balance;
    }

    // Business methods with validation
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.printf("Deposited $%.2f. New balance: $%.2f%n", amount, balance);
        } else {
            System.out.println("Deposit amount must be positive");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.printf("Withdrew $%.2f. New balance: $%.2f%n", amount, balance);
        } else if (amount > balance) {
            System.out.println("Insufficient funds");
        } else {
            System.out.println("Withdrawal amount must be positive");
        }
    }

    @Override
    public String toString() {
        return String.format("BankAccount{owner='%s', balance=$%.2f}", owner, balance);
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount("Alice", 1000);

        System.out.println(account);
        account.deposit(500);
        account.withdraw(200);
        account.withdraw(2000);  // Insufficient funds
        System.out.println("Final balance: $" + account.getBalance());
    }
}
```

### Inheritance

```java
// Base class
class Animal {
    protected String name;
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void eat() {
        System.out.println(name + " is eating");
    }

    public void sleep() {
        System.out.println(name + " is sleeping");
    }

    @Override
    public String toString() {
        return name + " (age: " + age + ")";
    }
}

// Derived class
class Cat extends Animal {
    private boolean isIndoor;

    public Cat(String name, int age, boolean isIndoor) {
        super(name, age);  // Call parent constructor
        this.isIndoor = isIndoor;
    }

    // New method specific to Cat
    public void purr() {
        System.out.println(name + " is purring");
    }

    // Override parent method
    @Override
    public void eat() {
        System.out.println(name + " is eating cat food");
    }

    @Override
    public String toString() {
        return super.toString() + " [" + (isIndoor ? "indoor" : "outdoor") + " cat]";
    }
}

// Another derived class
class Fish extends Animal {
    private String waterType;

    public Fish(String name, int age, String waterType) {
        super(name, age);
        this.waterType = waterType;
    }

    public void swim() {
        System.out.println(name + " is swimming in " + waterType + " water");
    }

    @Override
    public void sleep() {
        System.out.println(name + " sleeps with eyes open");
    }
}

// Main class to test inheritance
public class InheritanceExample {
    public static void main(String[] args) {
        Cat cat = new Cat("Whiskers", 3, true);
        Fish fish = new Fish("Nemo", 1, "saltwater");

        cat.eat();      // Overridden method
        cat.sleep();    // Inherited method
        cat.purr();     // Cat-specific method
        System.out.println(cat);

        fish.eat();     // Inherited method
        fish.sleep();   // Overridden method
        fish.swim();    // Fish-specific method

        // Polymorphism
        Animal[] animals = {cat, fish};
        System.out.println("\nAll animals:");
        for (Animal animal : animals) {
            animal.eat();   // Calls the appropriate overridden method
        }
    }
}
```

### Interfaces

```java
// Interface definition
interface Drawable {
    void draw();           // Abstract method (no body)
    double getArea();      // Abstract method

    // Default method (Java 8+)
    default void describe() {
        System.out.println("This is a drawable shape with area: " + getArea());
    }
}

// Implementing the interface
class Circle implements Drawable {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a circle with radius " + radius);
    }

    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
}

class Rectangle implements Drawable {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a rectangle " + width + "x" + height);
    }

    @Override
    public double getArea() {
        return width * height;
    }
}

public class InterfaceExample {
    public static void main(String[] args) {
        Drawable[] shapes = {
            new Circle(5),
            new Rectangle(4, 6)
        };

        for (Drawable shape : shapes) {
            shape.draw();
            shape.describe();  // Uses default method
            System.out.printf("Area: %.2f%n%n", shape.getArea());
        }
    }
}
```

---

## Practice Exercises

### Exercise 1: Temperature Converter
Create a program that converts between Celsius and Fahrenheit.

```java
import java.util.Scanner;

public class TemperatureConverter {
    static double celsiusToFahrenheit(double celsius) {
        return (celsius * 9.0 / 5.0) + 32;
    }

    static double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5.0 / 9.0;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Temperature Converter");
        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");
        System.out.print("Choose option (1 or 2): ");
        int choice = scanner.nextInt();

        System.out.print("Enter temperature: ");
        double temp = scanner.nextDouble();

        if (choice == 1) {
            System.out.printf("%.1f°C = %.1f°F%n", temp, celsiusToFahrenheit(temp));
        } else if (choice == 2) {
            System.out.printf("%.1f°F = %.1f°C%n", temp, fahrenheitToCelsius(temp));
        } else {
            System.out.println("Invalid option");
        }

        scanner.close();
    }
}
```

### Exercise 2: Simple Calculator
Build a calculator that handles basic operations.

```java
import java.util.Scanner;

public class Calculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first number: ");
        double num1 = scanner.nextDouble();

        System.out.print("Enter operator (+, -, *, /): ");
        char operator = scanner.next().charAt(0);

        System.out.print("Enter second number: ");
        double num2 = scanner.nextDouble();

        double result;

        switch (operator) {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 != 0) {
                    result = num1 / num2;
                } else {
                    System.out.println("Error: Division by zero");
                    scanner.close();
                    return;
                }
                break;
            default:
                System.out.println("Invalid operator");
                scanner.close();
                return;
        }

        System.out.printf("%.2f %c %.2f = %.2f%n", num1, operator, num2, result);
        scanner.close();
    }
}
```

### Exercise 3: Number Guessing Game
Create a game where the user guesses a random number.

```java
import java.util.Random;
import java.util.Scanner;

public class GuessingGame {
    public static void main(String[] args) {
        Random random = new Random();
        Scanner scanner = new Scanner(System.in);

        int secretNumber = random.nextInt(100) + 1;  // 1 to 100
        int attempts = 0;
        int maxAttempts = 7;

        System.out.println("I'm thinking of a number between 1 and 100.");
        System.out.println("You have " + maxAttempts + " attempts.");

        while (attempts < maxAttempts) {
            System.out.print("Enter your guess: ");
            int guess = scanner.nextInt();
            attempts++;

            if (guess == secretNumber) {
                System.out.println("Congratulations! You guessed it in " + attempts + " attempts!");
                scanner.close();
                return;
            } else if (guess < secretNumber) {
                System.out.println("Too low! " + (maxAttempts - attempts) + " attempts remaining.");
            } else {
                System.out.println("Too high! " + (maxAttempts - attempts) + " attempts remaining.");
            }
        }

        System.out.println("Game over! The number was " + secretNumber);
        scanner.close();
    }
}
```

### Exercise 4: Student Grade Manager
Build a class to manage student grades.

```java
import java.util.ArrayList;
import java.util.Collections;

public class Student {
    private String name;
    private ArrayList<Double> grades;

    public Student(String name) {
        this.name = name;
        this.grades = new ArrayList<>();
    }

    public void addGrade(double grade) {
        if (grade >= 0 && grade <= 100) {
            grades.add(grade);
        } else {
            System.out.println("Grade must be between 0 and 100");
        }
    }

    public double getAverage() {
        if (grades.isEmpty()) return 0;
        double sum = 0;
        for (double grade : grades) {
            sum += grade;
        }
        return sum / grades.size();
    }

    public double getHighest() {
        return grades.isEmpty() ? 0 : Collections.max(grades);
    }

    public double getLowest() {
        return grades.isEmpty() ? 0 : Collections.min(grades);
    }

    public String getLetterGrade() {
        double avg = getAverage();
        if (avg >= 90) return "A";
        if (avg >= 80) return "B";
        if (avg >= 70) return "C";
        if (avg >= 60) return "D";
        return "F";
    }

    @Override
    public String toString() {
        return String.format("%s - Average: %.1f (%s), Grades: %s",
            name, getAverage(), getLetterGrade(), grades);
    }

    public static void main(String[] args) {
        Student student1 = new Student("Alice");
        student1.addGrade(92);
        student1.addGrade(85);
        student1.addGrade(88);
        student1.addGrade(95);

        Student student2 = new Student("Bob");
        student2.addGrade(78);
        student2.addGrade(82);
        student2.addGrade(71);
        student2.addGrade(75);

        System.out.println(student1);
        System.out.printf("Highest: %.1f, Lowest: %.1f%n", student1.getHighest(), student1.getLowest());

        System.out.println(student2);
        System.out.printf("Highest: %.1f, Lowest: %.1f%n", student2.getHighest(), student2.getLowest());
    }
}
```
