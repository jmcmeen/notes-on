# Elementary PHP Programming Concepts

## Table of Contents

1. [Getting Started with PHP](#getting-started-with-php)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Arrays](#arrays)
9. [String Manipulation](#string-manipulation)
10. [Error Handling](#error-handling)
11. [File Operations](#file-operations)
12. [Classes and Objects](#classes-and-objects)
13. [Working with Forms and HTTP](#working-with-forms-and-http)
14. [Practice Exercises](#practice-exercises)
15. [Summary](#summary)

---

## Getting Started with PHP

### What is PHP?

PHP (PHP: Hypertext Preprocessor) is a server-side scripting language designed for web development. Key features:
- **Server-side**: Code runs on the server, sending HTML to the browser
- **Embedded in HTML**: PHP code can be mixed directly with HTML
- **Dynamically typed**: Variable types are determined at runtime
- **Extensive ecosystem**: Powers WordPress, Laravel, Drupal, and many CMS platforms
- **Built-in web features**: Native support for sessions, cookies, forms, and databases
- **Cross-platform**: Runs on Linux, Windows, macOS with Apache, Nginx, or built-in server

### Your First PHP Program

```php
<?php
// This is a comment
echo "Hello, World!\n";
?>
```

**Output:**
```
Hello, World!
```

### Embedded in HTML

```php
<!DOCTYPE html>
<html>
<head>
    <title>My PHP Page</title>
</head>
<body>
    <h1><?php echo "Hello from PHP!"; ?></h1>
    <p>Current time: <?= date("Y-m-d H:i:s") ?></p>
</body>
</html>
```

### Program Structure Explained

- **<?php ... ?>** - PHP opening and closing tags
- **<?= ... ?>** - Short echo tag (shorthand for `<?php echo ... ?>`)
- **echo** - Outputs one or more strings
- **print** - Similar to echo but returns 1 (can be used in expressions)
- **//** or **#** - Single-line comment
- **/* ... */** - Multi-line comment
- **;** - Statements must end with a semicolon

### Development Environment

- **XAMPP/MAMP/WAMP**: Bundles Apache, MySQL, and PHP for local development
- **Built-in server**: `php -S localhost:8000` (PHP 5.4+)
- **Composer**: Dependency manager for PHP
- **PHPStorm**: Full-featured IDE
- **VS Code**: Lightweight editor with PHP extensions

### Running PHP

```bash
# Run a PHP script from command line
php hello.php

# Start built-in development server
php -S localhost:8000

# Interactive shell
php -a
```

---

## Variables and Data Types

### Variable Declaration

All PHP variables start with a `$` sign. No type declaration is needed.

```php
<?php
// Declaring variables
$name = "Alice";
$age = 25;
$height = 5.6;
$isStudent = true;

echo "Name: $name\n";
echo "Age: $age\n";
echo "Height: $height\n";
echo "Is Student: " . ($isStudent ? "Yes" : "No") . "\n";
?>
```

### Data Types

```php
<?php
// 1. Integer
$integer = 42;
$negative = -10;
$hex = 0x1A;        // 26 in hexadecimal
$octal = 0755;       // 493 in octal
$binary = 0b1010;    // 10 in binary

echo gettype($integer) . "\n";  // "integer"

// 2. Float (double)
$float = 3.14;
$scientific = 2.5e3;  // 2500.0

echo gettype($float) . "\n";  // "double"

// 3. String
$single = 'Hello';            // Single quotes (no variable interpolation)
$double = "Hello, $name!";    // Double quotes (variable interpolation)
$heredoc = <<<EOT
This is a
multi-line string with $name
EOT;

$nowdoc = <<<'EOT'
This is a
multi-line string without interpolation
EOT;

// 4. Boolean
$isTrue = true;
$isFalse = false;

// 5. Array
$fruits = ["apple", "banana", "cherry"];
$assoc = ["name" => "Alice", "age" => 25];

// 6. NULL
$empty = null;
$unset = NULL;

// 7. Object (covered in Classes section)

// Type checking
var_dump($integer);    // int(42)
var_dump($float);      // float(3.14)
var_dump($isTrue);     // bool(true)
var_dump($empty);      // NULL
echo is_int($integer) ? "true" : "false";     // true
echo is_string($name) ? "true" : "false";     // true
echo is_null($empty) ? "true" : "false";      // true
echo isset($name) ? "true" : "false";         // true
echo empty("") ? "true" : "false";            // true
?>
```

### Type Casting

```php
<?php
// Explicit casting
$str = "42";
$num = (int) $str;         // 42
$flt = (float) "3.14";    // 3.14
$str2 = (string) 42;      // "42"
$bool = (bool) 1;         // true
$arr = (array) "hello";   // ["hello"]

// Type juggling (automatic conversion)
echo "5" + 3 . "\n";      // 8 (numeric addition)
echo "5" . 3 . "\n";      // "53" (string concatenation)
echo true + true . "\n";  // 2

// intval, floatval, strval
echo intval("42abc") . "\n";   // 42
echo floatval("3.14") . "\n";  // 3.14

// settype (modifies variable in place)
$var = "123";
settype($var, "integer");
var_dump($var);  // int(123)
?>
```

### Constants

```php
<?php
// define() function
define("PI", 3.14159);
define("COMPANY", "TechCorp");

echo PI . "\n";       // 3.14159
echo COMPANY . "\n";  // "TechCorp"

// const keyword (must be at compile time)
const MAX_SIZE = 100;
const VERSION = "1.0.0";

// Predefined constants
echo PHP_VERSION . "\n";
echo PHP_INT_MAX . "\n";
echo PHP_EOL;              // Platform-specific newline
echo PHP_OS . "\n";
?>
```

---

## Basic Operations

### Arithmetic Operators

```php
<?php
$a = 10;
$b = 3;

echo "10 + 3 = " . ($a + $b) . "\n";     // 13
echo "10 - 3 = " . ($a - $b) . "\n";     // 7
echo "10 * 3 = " . ($a * $b) . "\n";     // 30
echo "10 / 3 = " . ($a / $b) . "\n";     // 3.3333...
echo "10 % 3 = " . ($a % $b) . "\n";     // 1
echo "10 ** 3 = " . ($a ** $b) . "\n";   // 1000
echo "intdiv(10,3) = " . intdiv($a, $b) . "\n"; // 3

// Compound assignment
$x = 5;
$x += 3;   // 8
$x -= 2;   // 6
$x *= 2;   // 12
$x /= 4;   // 3
$x %= 2;   // 1
$x **= 3;  // 1

// Increment and decrement
$counter = 5;
echo $counter++ . "\n";  // 5 (post-increment)
echo $counter . "\n";    // 6
echo ++$counter . "\n";  // 7 (pre-increment)
echo $counter-- . "\n";  // 7 (post-decrement)
echo $counter . "\n";    // 6
?>
```

### Comparison Operators

```php
<?php
$x = 5;
$y = "5";

// Loose comparison (==) - type coercion
var_dump($x == $y);    // true
var_dump($x != $y);    // false

// Strict comparison (===) - no type coercion (PREFERRED)
var_dump($x === $y);   // false (different types)
var_dump($x !== $y);   // true

// Other comparisons
var_dump(5 < 10);      // true
var_dump(5 > 10);      // false
var_dump(5 <= 5);      // true
var_dump(5 >= 10);     // false

// Spaceship operator <=> (returns -1, 0, or 1)
echo (1 <=> 2) . "\n";   // -1
echo (2 <=> 2) . "\n";   // 0
echo (3 <=> 2) . "\n";   // 1

// Null coalescing operator ??
$username = $_GET["user"] ?? "Guest";
echo $username . "\n";

// Null coalescing assignment ??=
$config["theme"] ??= "light";  // Only assigns if null
?>
```

### Logical Operators

```php
<?php
$a = true;
$b = false;

var_dump($a && $b);    // false (AND)
var_dump($a || $b);    // true (OR)
var_dump(!$a);         // false (NOT)

// Alternative syntax
var_dump($a and $b);   // false
var_dump($a or $b);    // true
var_dump($a xor $b);   // true (exclusive or)

// Practical example
$age = 20;
$hasLicense = true;
$canDrive = ($age >= 18) && $hasLicense;
echo "Can drive: " . ($canDrive ? "Yes" : "No") . "\n";
?>
```

---

## Input and Output

### Output Functions

```php
<?php
// echo - outputs strings (no return value)
echo "Hello, World!\n";
echo "Hello", " ", "World\n";  // Multiple parameters

// print - outputs a string (returns 1)
print "Hello, World!\n";

// print_r - readable format for arrays/objects
$arr = ["apple", "banana", "cherry"];
print_r($arr);
// Array ( [0] => apple [1] => banana [2] => cherry )

// var_dump - detailed type and value info
var_dump($arr);
// array(3) { [0]=> string(5) "apple" [1]=> string(6) "banana" [2]=> string(6) "cherry" }

// var_export - outputs valid PHP code
var_export($arr);
// array ( 0 => 'apple', 1 => 'banana', 2 => 'cherry', )

// printf / sprintf - formatted output
$name = "Alice";
$age = 25;
$gpa = 3.85;

printf("Name: %s, Age: %d, GPA: %.2f\n", $name, $age, $gpa);
$formatted = sprintf("Name: %s, Age: %d", $name, $age);
echo $formatted . "\n";
?>
```

### Command-Line Input

```php
<?php
// Reading from stdin
echo "What's your name? ";
$name = trim(fgets(STDIN));
echo "Hello, $name!\n";

// Reading with readline (if available)
$age = readline("How old are you? ");
echo "You are $age years old\n";

// Command-line arguments
// php script.php arg1 arg2
echo "Script: $argv[0]\n";
echo "Arguments: " . ($argc - 1) . "\n";
for ($i = 1; $i < $argc; $i++) {
    echo "Arg $i: $argv[$i]\n";
}
?>
```

---

## Conditional Statements

### if, elseif, else

```php
<?php
// Basic if
$age = 18;

if ($age >= 18) {
    echo "You are an adult\n";
    echo "You can vote\n";
}

// if-else
$temperature = 25;

if ($temperature > 30) {
    echo "It's hot outside\n";
} else {
    echo "It's not too hot\n";
}

// if-elseif-else
$score = 85;

if ($score >= 90) {
    $grade = "A";
} elseif ($score >= 80) {
    $grade = "B";
} elseif ($score >= 70) {
    $grade = "C";
} elseif ($score >= 60) {
    $grade = "D";
} else {
    $grade = "F";
}

echo "Your grade is: $grade\n";
?>
```

### switch Statements

```php
<?php
$dayNumber = 3;

switch ($dayNumber) {
    case 1:
        $dayName = "Monday";
        break;
    case 2:
        $dayName = "Tuesday";
        break;
    case 3:
        $dayName = "Wednesday";
        break;
    case 4:
        $dayName = "Thursday";
        break;
    case 5:
        $dayName = "Friday";
        break;
    case 6:
    case 7:
        $dayName = "Weekend";
        break;
    default:
        $dayName = "Invalid day";
}

echo "Day $dayNumber is $dayName\n";

// match expression (PHP 8.0+) - strict comparison, returns a value
$status = 404;
$message = match ($status) {
    200 => "OK",
    301 => "Moved Permanently",
    404 => "Not Found",
    500 => "Internal Server Error",
    default => "Unknown Status"
};

echo "$status: $message\n";

// match with multiple conditions
$month = 6;
$season = match (true) {
    in_array($month, [12, 1, 2]) => "Winter",
    in_array($month, [3, 4, 5]) => "Spring",
    in_array($month, [6, 7, 8]) => "Summer",
    in_array($month, [9, 10, 11]) => "Fall",
    default => "Invalid month"
};

echo "Month $month is in $season\n";
?>
```

### Ternary Operator

```php
<?php
$age = 20;

// Ternary
$status = ($age >= 18) ? "Adult" : "Minor";
echo "Status: $status\n";

// Elvis operator (?:) - shorthand for null/falsy check
$username = "" ?: "Anonymous";
echo "Username: $username\n";  // "Anonymous"

// Null coalescing (??) - only checks null
$config = null;
$theme = $config ?? "light";
echo "Theme: $theme\n";  // "light"
?>
```

---

## Loops

### for Loops

```php
<?php
// Basic for loop
echo "Counting to 5:\n";
for ($i = 1; $i <= 5; $i++) {
    echo "Count: $i\n";
}

// Even numbers
echo "\nEven numbers from 2 to 10:\n";
for ($i = 2; $i <= 10; $i += 2) {
    echo "$i\n";
}

// Counting backwards
echo "\nCountdown:\n";
for ($i = 5; $i >= 1; $i--) {
    echo "$i\n";
}
echo "Blast off!\n";
?>
```

### foreach Loops

```php
<?php
// Iterate over indexed array
$fruits = ["apple", "banana", "cherry"];

echo "Fruits:\n";
foreach ($fruits as $fruit) {
    echo "- $fruit\n";
}

// With index
foreach ($fruits as $index => $fruit) {
    echo "$index: $fruit\n";
}

// Iterate over associative array
$person = ["name" => "Alice", "age" => 25, "city" => "NYC"];

echo "\nPerson:\n";
foreach ($person as $key => $value) {
    echo "$key: $value\n";
}

// Modify values by reference
$numbers = [1, 2, 3, 4, 5];
foreach ($numbers as &$num) {
    $num *= 2;
}
unset($num);  // Always unset reference after foreach
print_r($numbers);  // [2, 4, 6, 8, 10]
?>
```

### while and do-while Loops

```php
<?php
// Basic while loop
$count = 0;
while ($count < 3) {
    echo "Count is: $count\n";
    $count++;
}

// do-while loop
$input = "";
do {
    echo "Enter 'quit' to exit: ";
    $input = trim(fgets(STDIN));
    echo "You entered: $input\n";
} while ($input !== "quit");

echo "Goodbye!\n";
?>
```

### Loop Control

```php
<?php
// break
echo "Numbers with break:\n";
for ($i = 0; $i < 10; $i++) {
    if ($i === 5) break;
    echo "$i ";
}
echo "\n";

// continue
echo "Skip multiples of 3:\n";
for ($i = 0; $i < 10; $i++) {
    if ($i % 3 === 0) continue;
    echo "$i ";
}
echo "\n";

// break with level (break out of nested loops)
for ($i = 0; $i < 3; $i++) {
    for ($j = 0; $j < 3; $j++) {
        if ($i === 1 && $j === 1) break 2;  // Break 2 levels
        echo "i=$i, j=$j\n";
    }
}
?>
```

---

## Functions

### Defining Functions

```php
<?php
// Basic function
function sayHello(): void {
    echo "Hello from a function!\n";
}

// Function with parameters
function greetPerson(string $name): void {
    echo "Hello, $name!\n";
}

// Function with return value
function addNumbers(int $a, int $b): int {
    return $a + $b;
}

// Function with type hints and return type
function calculateArea(float $length, float $width): float {
    return $length * $width;
}

// Calling functions
sayHello();
greetPerson("Alice");
echo "5 + 3 = " . addNumbers(5, 3) . "\n";
echo "Area: " . number_format(calculateArea(4.5, 6.2), 2) . "\n";
?>
```

### Default Parameters and Named Arguments

```php
<?php
// Default parameters
function greet(string $name, string $greeting = "Hello"): void {
    echo "$greeting, $name!\n";
}

greet("Alice");          // "Hello, Alice!"
greet("Bob", "Hi");     // "Hi, Bob!"

// Named arguments (PHP 8.0+)
function createUser(string $name, int $age, string $role = "user"): void {
    echo "Name: $name, Age: $age, Role: $role\n";
}

createUser(name: "Alice", age: 25);
createUser(age: 30, name: "Bob", role: "admin");

// Variadic functions
function sumAll(int ...$numbers): int {
    return array_sum($numbers);
}

echo "Sum: " . sumAll(1, 2, 3) . "\n";        // 6
echo "Sum: " . sumAll(1, 2, 3, 4, 5) . "\n";  // 15

// Spread operator
$nums = [1, 2, 3, 4, 5];
echo "Sum: " . sumAll(...$nums) . "\n";  // 15
?>
```

### Anonymous Functions and Arrow Functions

```php
<?php
// Anonymous function (closure)
$greet = function(string $name): string {
    return "Hello, $name!";
};

echo $greet("Alice") . "\n";

// Using variables from outer scope
$prefix = "Dear";
$formalGreet = function(string $name) use ($prefix): string {
    return "$prefix $name";
};

echo $formalGreet("Alice") . "\n";

// Arrow function (PHP 7.4+) - auto-captures outer variables
$multiplier = 3;
$multiply = fn($x) => $x * $multiplier;

echo $multiply(5) . "\n";  // 15

// Higher-order functions
$numbers = [1, 2, 3, 4, 5];

$doubled = array_map(fn($n) => $n * 2, $numbers);
$evens = array_filter($numbers, fn($n) => $n % 2 === 0);
$sum = array_reduce($numbers, fn($carry, $n) => $carry + $n, 0);

print_r($doubled);  // [2, 4, 6, 8, 10]
print_r($evens);     // [2, 4]
echo "Sum: $sum\n";  // 15
?>
```

---

## Arrays

### Indexed Arrays

```php
<?php
// Creating arrays
$fruits = ["apple", "banana", "cherry"];
$numbers = array(1, 2, 3, 4, 5);
$empty = [];
$filled = array_fill(0, 5, 0);  // [0, 0, 0, 0, 0]
$range = range(1, 10);           // [1, 2, 3, ..., 10]

// Accessing elements
echo $fruits[0] . "\n";              // "apple"
echo $fruits[count($fruits) - 1] . "\n"; // "cherry"

// Modifying
$fruits[] = "date";        // Append
$fruits[1] = "blueberry";  // Replace
echo count($fruits) . "\n"; // 4

// Array functions
$arr = [3, 1, 4, 1, 5, 9, 2, 6];

sort($arr);                    // Sort ascending (modifies in place)
print_r($arr);

rsort($arr);                   // Sort descending
array_push($arr, 10);         // Add to end
array_pop($arr);               // Remove from end
array_unshift($arr, 0);       // Add to beginning
array_shift($arr);             // Remove from beginning

echo in_array(4, $arr) ? "found\n" : "not found\n";
echo array_search(4, $arr) . "\n";  // Index of 4

$sliced = array_slice($arr, 1, 3);  // Extract portion
$merged = array_merge($arr, [10, 11, 12]);
$unique = array_unique([1, 2, 2, 3, 3, 4]);
$reversed = array_reverse($arr);
?>
```

### Associative Arrays

```php
<?php
// Creating associative arrays
$person = [
    "name" => "Alice",
    "age" => 25,
    "city" => "New York"
];

// Accessing values
echo $person["name"] . "\n";  // "Alice"

// Modifying
$person["age"] = 26;
$person["email"] = "alice@example.com";

// Removing
unset($person["email"]);

// Checking keys
echo array_key_exists("name", $person) ? "exists\n" : "not found\n";
echo isset($person["name"]) ? "set\n" : "not set\n";

// Getting keys and values
$keys = array_keys($person);
$values = array_values($person);

// Iterating
foreach ($person as $key => $value) {
    echo "$key: $value\n";
}

// Merging associative arrays
$defaults = ["theme" => "light", "lang" => "en", "fontSize" => 14];
$userPrefs = ["theme" => "dark", "fontSize" => 16];
$settings = array_merge($defaults, $userPrefs);
print_r($settings);
// theme => dark, lang => en, fontSize => 16
?>
```

### Array Utility Functions

```php
<?php
$numbers = [3, 1, 4, 1, 5, 9, 2, 6];

// Math operations
echo "Sum: " . array_sum($numbers) . "\n";
echo "Product: " . array_product([1, 2, 3, 4]) . "\n";
echo "Min: " . min($numbers) . "\n";
echo "Max: " . max($numbers) . "\n";

// Transform
$doubled = array_map(fn($n) => $n * 2, $numbers);
$evens = array_filter($numbers, fn($n) => $n % 2 === 0);
$sum = array_reduce($numbers, fn($carry, $n) => $carry + $n, 0);

// Combine and split
$keys = ["a", "b", "c"];
$values = [1, 2, 3];
$combined = array_combine($keys, $values);  // ["a"=>1, "b"=>2, "c"=>3]

[$first, $second] = [10, 20];  // Array destructuring
echo "First: $first, Second: $second\n";

// Sorting associative arrays
$scores = ["Alice" => 95, "Bob" => 87, "Charlie" => 92];
asort($scores);   // Sort by value, keep keys
arsort($scores);  // Sort by value descending
ksort($scores);   // Sort by key
krsort($scores);  // Sort by key descending

// Custom sort
usort($numbers, fn($a, $b) => $b - $a);  // Sort descending
?>
```

---

## String Manipulation

### String Basics

```php
<?php
$text = "Hello, World!";

// String functions
echo strlen($text) . "\n";          // 13
echo strtoupper($text) . "\n";     // "HELLO, WORLD!"
echo strtolower($text) . "\n";     // "hello, world!"
echo ucfirst("hello") . "\n";      // "Hello"
echo ucwords("hello world") . "\n"; // "Hello World"

// Searching
echo strpos($text, "World") . "\n";    // 7
echo strrpos($text, "l") . "\n";       // 10
echo substr_count($text, "l") . "\n";  // 3

// Checking
echo str_starts_with($text, "Hello") ? "yes\n" : "no\n";  // PHP 8.0+
echo str_ends_with($text, "!") ? "yes\n" : "no\n";
echo str_contains($text, "World") ? "yes\n" : "no\n";
?>
```

### String Manipulation

```php
<?php
// Substring
$text = "Hello, World!";
echo substr($text, 0, 5) . "\n";    // "Hello"
echo substr($text, 7) . "\n";        // "World!"
echo substr($text, -6) . "\n";       // "orld!"

// Replacing
echo str_replace("World", "PHP", $text) . "\n";
echo str_ireplace("hello", "Hi", $text) . "\n";  // Case-insensitive

// Trimming
$padded = "  Hello, World!  ";
echo trim($padded) . "\n";
echo ltrim($padded) . "\n";
echo rtrim($padded) . "\n";

// Splitting and joining
$csv = "apple,banana,cherry,date";
$parts = explode(",", $csv);
print_r($parts);

$joined = implode(" | ", $parts);
echo $joined . "\n";  // "apple | banana | cherry | date"

// Padding
echo str_pad("5", 3, "0", STR_PAD_LEFT) . "\n";   // "005"
echo str_pad("Hi", 10, ".", STR_PAD_RIGHT) . "\n"; // "Hi........"

// Repeating
echo str_repeat("ha", 3) . "\n";  // "hahaha"

// Reversing
echo strrev("Hello") . "\n";  // "olleH"

// String interpolation
$name = "Alice";
$age = 25;
echo "Name: $name, Age: $age\n";
echo "Array: {$parts[0]}\n";

// Heredoc (with interpolation)
echo <<<EOT
Hello, $name!
You are $age years old.
EOT;
echo "\n";

// Nowdoc (no interpolation)
echo <<<'EOT'
This is a literal $string
with no variable interpolation.
EOT;
echo "\n";
?>
```

---

## Error Handling

### Try-Catch

```php
<?php
// Basic try-catch
try {
    $result = 10 / 0;  // Warning in PHP, not an exception
    echo $result . "\n";

    throw new Exception("Something went wrong");
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n";
}

// Try-catch-finally
try {
    $data = json_decode('invalid json', true, 512, JSON_THROW_ON_ERROR);
} catch (JsonException $e) {
    echo "JSON Error: " . $e->getMessage() . "\n";
} finally {
    echo "This always runs\n";
}

// Multiple catch blocks
try {
    // Some risky operation
    $value = random_int(0, 1);
    if ($value === 0) {
        throw new InvalidArgumentException("Invalid value");
    } else {
        throw new RuntimeException("Runtime problem");
    }
} catch (InvalidArgumentException $e) {
    echo "Invalid argument: " . $e->getMessage() . "\n";
} catch (RuntimeException $e) {
    echo "Runtime error: " . $e->getMessage() . "\n";
} catch (Exception $e) {
    echo "General error: " . $e->getMessage() . "\n";
}

// Union catch types (PHP 8.0+)
try {
    // ...
} catch (InvalidArgumentException | RuntimeException $e) {
    echo "Caught: " . $e->getMessage() . "\n";
}
?>
```

### Custom Exceptions

```php
<?php
class ValidationException extends Exception {
    private string $field;

    public function __construct(string $field, string $message, int $code = 0) {
        $this->field = $field;
        parent::__construct($message, $code);
    }

    public function getField(): string {
        return $this->field;
    }
}

function validateAge(int $age): void {
    if ($age < 0 || $age > 150) {
        throw new ValidationException("age", "Age must be between 0 and 150");
    }
}

try {
    validateAge(200);
} catch (ValidationException $e) {
    echo "Field '{$e->getField()}': {$e->getMessage()}\n";
}
?>
```

---

## File Operations

### Reading and Writing Files

```php
<?php
$filename = "example.txt";

// Writing to a file
file_put_contents($filename, "Hello, World!\nLine 2\nLine 3\n");
echo "File written\n";

// Reading entire file as string
$content = file_get_contents($filename);
echo "Content:\n$content";

// Reading file into array (one element per line)
$lines = file($filename, FILE_IGNORE_NEW_LINES);
foreach ($lines as $i => $line) {
    echo ($i + 1) . ": $line\n";
}

// Appending to a file
file_put_contents($filename, "Appended line\n", FILE_APPEND);

// Reading line by line with fopen/fgets
$handle = fopen($filename, "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        echo ">> " . trim($line) . "\n";
    }
    fclose($handle);
}

// File information
echo "Exists: " . (file_exists($filename) ? "yes" : "no") . "\n";
echo "Size: " . filesize($filename) . " bytes\n";
echo "Is file: " . (is_file($filename) ? "yes" : "no") . "\n";
echo "Is dir: " . (is_dir($filename) ? "yes" : "no") . "\n";

// CSV files
$data = [
    ["Name", "Age", "City"],
    ["Alice", 25, "NYC"],
    ["Bob", 30, "LA"]
];

$fp = fopen("data.csv", "w");
foreach ($data as $row) {
    fputcsv($fp, $row);
}
fclose($fp);

// Reading CSV
$fp = fopen("data.csv", "r");
while (($row = fgetcsv($fp)) !== false) {
    echo implode(", ", $row) . "\n";
}
fclose($fp);

// Cleanup
unlink($filename);
unlink("data.csv");
?>
```

---

## Classes and Objects

### Basic Class

```php
<?php
class Dog {
    // Properties
    public string $name;
    public string $breed;
    public int $age;

    // Constructor
    public function __construct(string $name, string $breed, int $age) {
        $this->name = $name;
        $this->breed = $breed;
        $this->age = $age;
    }

    // Methods
    public function bark(): void {
        echo "{$this->name} says: Woof!\n";
    }

    public function describe(): void {
        echo "{$this->name} is a {$this->age}-year-old {$this->breed}\n";
    }

    public function getAgeInHumanYears(): int {
        return $this->age * 7;
    }

    // Magic method for string representation
    public function __toString(): string {
        return "Dog({$this->name}, {$this->breed}, {$this->age})";
    }
}

// Creating objects
$dog1 = new Dog("Buddy", "Golden Retriever", 3);
$dog2 = new Dog("Max", "German Shepherd", 5);

$dog1->bark();
$dog2->describe();
echo "$dog1\n";
echo "Human years: " . $dog1->getAgeInHumanYears() . "\n";
?>
```

### Constructor Promotion and Visibility

```php
<?php
// Constructor property promotion (PHP 8.0+)
class BankAccount {
    public function __construct(
        private string $owner,
        private float $balance = 0.0
    ) {
        if ($balance < 0) {
            $this->balance = 0;
            echo "Initial balance cannot be negative. Set to 0.\n";
        }
    }

    public function getOwner(): string {
        return $this->owner;
    }

    public function getBalance(): float {
        return $this->balance;
    }

    public function deposit(float $amount): void {
        if ($amount > 0) {
            $this->balance += $amount;
            printf("Deposited \$%.2f. New balance: \$%.2f\n", $amount, $this->balance);
        }
    }

    public function withdraw(float $amount): void {
        if ($amount > 0 && $amount <= $this->balance) {
            $this->balance -= $amount;
            printf("Withdrew \$%.2f. New balance: \$%.2f\n", $amount, $this->balance);
        } elseif ($amount > $this->balance) {
            echo "Insufficient funds\n";
        }
    }
}

$account = new BankAccount("Alice", 1000);
$account->deposit(500);
$account->withdraw(200);
$account->withdraw(2000);
printf("Final balance: \$%.2f\n", $account->getBalance());
?>
```

### Inheritance and Interfaces

```php
<?php
// Base class
class Animal {
    public function __construct(
        protected string $name,
        protected int $age
    ) {}

    public function eat(): void {
        echo "{$this->name} is eating\n";
    }

    public function __toString(): string {
        return "{$this->name} (age: {$this->age})";
    }
}

// Child class
class Cat extends Animal {
    public function __construct(
        string $name,
        int $age,
        private bool $isIndoor = true
    ) {
        parent::__construct($name, $age);
    }

    public function purr(): void {
        echo "{$this->name} is purring\n";
    }

    // Override parent method
    public function eat(): void {
        echo "{$this->name} is eating cat food\n";
    }
}

// Interface
interface Drawable {
    public function draw(): void;
    public function getArea(): float;
}

class Circle implements Drawable {
    public function __construct(private float $radius) {}

    public function draw(): void {
        echo "Drawing circle with radius {$this->radius}\n";
    }

    public function getArea(): float {
        return M_PI * $this->radius ** 2;
    }
}

// Using
$cat = new Cat("Whiskers", 3);
$cat->eat();
$cat->purr();

$circle = new Circle(5);
$circle->draw();
printf("Area: %.2f\n", $circle->getArea());
?>
```

---

## Working with Forms and HTTP

### Handling GET and POST Requests

```php
<!-- form.html -->
<form method="POST" action="process.php">
    <label>Name: <input type="text" name="name"></label><br>
    <label>Email: <input type="email" name="email"></label><br>
    <label>Age: <input type="number" name="age"></label><br>
    <button type="submit">Submit</button>
</form>
```

```php
<?php
// process.php

// Check request method
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get POST data (with sanitization)
    $name = htmlspecialchars(trim($_POST["name"] ?? ""));
    $email = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL);
    $age = filter_input(INPUT_POST, "age", FILTER_VALIDATE_INT);

    if ($name && $email && $age) {
        echo "Name: $name<br>";
        echo "Email: $email<br>";
        echo "Age: $age<br>";
    } else {
        echo "Invalid input";
    }
}

// GET parameters (e.g., page.php?search=hello&page=2)
$search = htmlspecialchars($_GET["search"] ?? "");
$page = filter_input(INPUT_GET, "page", FILTER_VALIDATE_INT) ?: 1;

echo "Search: $search, Page: $page\n";

// Working with JSON
header("Content-Type: application/json");
$data = ["status" => "success", "message" => "Data received"];
echo json_encode($data);

// Reading JSON input
$input = json_decode(file_get_contents("php://input"), true);
?>
```

### Sessions and Cookies

```php
<?php
// Sessions
session_start();

// Set session data
$_SESSION["username"] = "Alice";
$_SESSION["logged_in"] = true;

// Read session data
if (isset($_SESSION["logged_in"]) && $_SESSION["logged_in"]) {
    echo "Welcome back, " . $_SESSION["username"] . "\n";
}

// Destroy session
// session_destroy();

// Cookies
setcookie("theme", "dark", time() + (86400 * 30), "/");  // 30 days

// Read cookie
$theme = $_COOKIE["theme"] ?? "light";
echo "Theme: $theme\n";
?>
```

---

## Practice Exercises

### Exercise 1: Temperature Converter

```php
<?php
function celsiusToFahrenheit(float $celsius): float {
    return ($celsius * 9.0 / 5.0) + 32;
}

function fahrenheitToCelsius(float $fahrenheit): float {
    return ($fahrenheit - 32) * 5.0 / 9.0;
}

echo "0°C = " . celsiusToFahrenheit(0) . "°F\n";
echo "100°C = " . celsiusToFahrenheit(100) . "°F\n";
echo "72°F = " . number_format(fahrenheitToCelsius(72), 1) . "°C\n";
?>
```

### Exercise 2: Simple Calculator

```php
<?php
function calculate(float $a, string $op, float $b): float|string {
    return match ($op) {
        "+" => $a + $b,
        "-" => $a - $b,
        "*" => $a * $b,
        "/" => $b != 0 ? $a / $b : "Error: Division by zero",
        default => "Error: Invalid operator"
    };
}

echo "5 + 3 = " . calculate(5, "+", 3) . "\n";
echo "10 / 3 = " . number_format(calculate(10, "/", 3), 2) . "\n";
echo "10 / 0 = " . calculate(10, "/", 0) . "\n";
?>
```

### Exercise 3: Student Grade Manager

```php
<?php
class Student {
    private array $grades = [];

    public function __construct(private string $name) {}

    public function addGrade(float $grade): void {
        if ($grade >= 0 && $grade <= 100) {
            $this->grades[] = $grade;
        }
    }

    public function getAverage(): float {
        return empty($this->grades) ? 0 : array_sum($this->grades) / count($this->grades);
    }

    public function getLetterGrade(): string {
        $avg = $this->getAverage();
        return match (true) {
            $avg >= 90 => "A",
            $avg >= 80 => "B",
            $avg >= 70 => "C",
            $avg >= 60 => "D",
            default => "F"
        };
    }

    public function __toString(): string {
        return sprintf("%s - Average: %.1f (%s), Grades: [%s]",
            $this->name,
            $this->getAverage(),
            $this->getLetterGrade(),
            implode(", ", $this->grades)
        );
    }
}

$student = new Student("Alice");
$student->addGrade(92);
$student->addGrade(85);
$student->addGrade(88);
$student->addGrade(95);

echo $student . "\n";
// Alice - Average: 90.0 (A), Grades: [92, 85, 88, 95]
?>
```

---

## Summary

These notes cover the fundamental concepts of PHP:

1. **Variables and Types**: `$` prefix, dynamic typing, type casting, constants
2. **Operations**: Arithmetic, comparison (`===` preferred), spaceship operator (`<=>`), null coalescing (`??`)
3. **Control Flow**: if/elseif/else, switch, match expressions (PHP 8.0+), ternary
4. **Loops**: for, foreach (with key/value and references), while, do-while
5. **Functions**: Type hints, default parameters, named arguments, variadic, arrow functions
6. **Arrays**: Indexed and associative arrays, array functions (map, filter, reduce, sort)
7. **Strings**: Interpolation, heredoc/nowdoc, string functions, regex support
8. **Error Handling**: try/catch/finally, custom exceptions, union catch types
9. **File Operations**: file_get_contents/file_put_contents, fopen/fgets, CSV handling
10. **OOP**: Classes, constructor promotion, inheritance, interfaces
11. **Web Features**: GET/POST handling, input sanitization, sessions, cookies, JSON

### Next Steps

1. Practice the exercises and build small web applications
2. Learn about Composer for dependency management
3. Explore the Laravel or Symfony frameworks
4. Study database integration with PDO or an ORM like Eloquent
5. Learn about PHP testing with PHPUnit

### Additional Resources

- **PHP Manual**: https://www.php.net/manual/en/
- **PHP: The Right Way**: https://phptherightway.com/
- **Laravel Documentation**: https://laravel.com/docs
- **Composer**: https://getcomposer.org/
- **Practice Problems**: https://exercism.org/tracks/php
