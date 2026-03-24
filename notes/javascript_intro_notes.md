# Elementary JavaScript Programming Concepts

## Table of Contents

1. [Getting Started with JavaScript](#getting-started-with-javascript)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Arrays](#arrays)
9. [Objects](#objects)
10. [String Manipulation](#string-manipulation)
11. [Error Handling](#error-handling)
12. [DOM Manipulation](#dom-manipulation)
13. [Asynchronous JavaScript](#asynchronous-javascript)
14. [Modules](#modules)
15. [Practice Exercises](#practice-exercises)
16. [Summary](#summary)

---

## Getting Started with JavaScript

### What is JavaScript?

JavaScript is a dynamic, interpreted programming language that powers the interactive web. Key features:
- **Multi-paradigm**: Supports object-oriented, functional, and event-driven programming
- **Dynamically typed**: Variable types are determined at runtime
- **First-class functions**: Functions are treated as values and can be passed around
- **Prototype-based**: Uses prototypal inheritance rather than classical inheritance
- **Ubiquitous**: Runs in every web browser and on servers via Node.js
- **Event-driven**: Built around an event loop for non-blocking I/O

### Your First JavaScript Program

**In the browser (browser console or HTML file):**
```javascript
// This is a comment
console.log("Hello, World!");
```

**In an HTML file:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My First JS</title>
</head>
<body>
    <script>
        console.log("Hello, World!");
        document.write("Hello from JavaScript!");
    </script>
</body>
</html>
```

**With Node.js (hello.js):**
```javascript
console.log("Hello, World!");
```

```bash
node hello.js
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **console.log()** - Prints output to the console
- **document.write()** - Writes directly to the HTML page (avoid in production)
- **//** - Single-line comment
- **/* ... */** - Multi-line comment
- **;** - Semicolons are optional but recommended for clarity

### Development Environment

- **Browser DevTools**: Built into Chrome, Firefox, Edge (press F12)
- **Visual Studio Code**: Lightweight editor with excellent JS support
- **Node.js**: JavaScript runtime for server-side execution
- **npm**: Package manager bundled with Node.js

---

## Variables and Data Types

### Variable Declaration

JavaScript has three ways to declare variables: `var`, `let`, and `const`.

```javascript
// let - block-scoped, can be reassigned (preferred for mutable variables)
let name = "Alice";
let age = 25;
name = "Bob";  // OK

// const - block-scoped, cannot be reassigned (preferred for constants)
const PI = 3.14159;
const COMPANY = "TechCorp";
// PI = 3.14;  // ERROR: Assignment to constant variable

// var - function-scoped, older style (avoid in modern code)
var oldStyle = "not recommended";

console.log(name);   // "Bob"
console.log(age);    // 25
console.log(PI);     // 3.14159
```

### Primitive Data Types

```javascript
// 1. Number (integers and floats are the same type)
let integer = 42;
let float = 3.14;
let negative = -10;
let infinity = Infinity;
let notANumber = NaN;

console.log(typeof integer);     // "number"
console.log(typeof float);       // "number"
console.log(0.1 + 0.2);          // 0.30000000000000004 (floating point!)
console.log(Number.isInteger(42)); // true

// 2. BigInt (for very large integers, ES2020+)
let big = 9007199254740991n;
let anotherBig = BigInt("12345678901234567890");

// 3. String
let greeting = "Hello";
let name2 = 'Alice';               // Single or double quotes
let template = `Hello, ${name2}!`; // Template literal (backticks)

console.log(typeof greeting);  // "string"
console.log(template);         // "Hello, Alice!"

// 4. Boolean
let isActive = true;
let isDeleted = false;

console.log(typeof isActive);  // "boolean"

// 5. undefined (declared but not assigned)
let notAssigned;
console.log(notAssigned);      // undefined
console.log(typeof notAssigned); // "undefined"

// 6. null (intentionally empty)
let emptyValue = null;
console.log(emptyValue);       // null
console.log(typeof emptyValue); // "object" (historical quirk)

// 7. Symbol (unique identifier, ES2015+)
let sym1 = Symbol("description");
let sym2 = Symbol("description");
console.log(sym1 === sym2);    // false (always unique)
```

### Type Coercion and Checking

```javascript
// JavaScript performs automatic type coercion
console.log("5" + 3);     // "53" (string concatenation)
console.log("5" - 3);     // 2 (numeric subtraction)
console.log("5" * 2);     // 10 (numeric multiplication)
console.log(true + 1);    // 2
console.log(false + 1);   // 1

// Explicit conversion
let str = "42";
let num = Number(str);       // 42
let parsed = parseInt("42px"); // 42
let floated = parseFloat("3.14"); // 3.14
let back = String(42);      // "42"
let bool = Boolean(0);      // false

// Falsy values: false, 0, "", null, undefined, NaN
// Truthy values: everything else (including "0", [], {})
console.log(Boolean(""));    // false
console.log(Boolean("0"));   // true
console.log(Boolean([]));    // true

// typeof operator
console.log(typeof 42);         // "number"
console.log(typeof "hello");    // "string"
console.log(typeof true);       // "boolean"
console.log(typeof undefined);  // "undefined"
console.log(typeof null);       // "object" (bug, kept for compatibility)
console.log(typeof [1, 2]);     // "object"
console.log(typeof {a: 1});     // "object"
console.log(Array.isArray([1, 2])); // true
```

---

## Basic Operations

### Arithmetic Operators

```javascript
let a = 10;
let b = 3;

// Basic arithmetic
console.log(a + b);    // 13
console.log(a - b);    // 7
console.log(a * b);    // 30
console.log(a / b);    // 3.3333... (always floating point)
console.log(a % b);    // 1 (remainder)
console.log(a ** b);   // 1000 (exponentiation, ES2016+)

// Integer division (use Math.floor or Math.trunc)
console.log(Math.floor(a / b));  // 3
console.log(Math.trunc(-10 / 3)); // -3

// Compound assignment
let x = 5;
x += 3;   // x = 8
x -= 2;   // x = 6
x *= 2;   // x = 12
x /= 4;   // x = 3
x %= 2;   // x = 1
x **= 3;  // x = 1

// Increment and decrement
let counter = 5;
console.log(counter++);  // 5 (returns then increments)
console.log(counter);    // 6
console.log(++counter);  // 7 (increments then returns)
console.log(counter--);  // 7 (returns then decrements)
console.log(counter);    // 6
```

### Comparison Operators

```javascript
let x = 5;
let y = "5";

// Loose equality (== / !=) - performs type coercion
console.log(x == y);    // true (coerces "5" to 5)
console.log(x != y);    // false

// Strict equality (=== / !==) - no type coercion (PREFERRED)
console.log(x === y);   // false (different types)
console.log(x !== y);   // true

// Other comparisons
console.log(5 < 10);    // true
console.log(5 > 10);    // false
console.log(5 <= 5);    // true
console.log(5 >= 10);   // false

// Always use === and !== to avoid coercion surprises
console.log(0 == false);    // true (surprising!)
console.log(0 === false);   // false (correct)
console.log("" == false);   // true (surprising!)
console.log("" === false);  // false (correct)
console.log(null == undefined);  // true
console.log(null === undefined); // false
```

### Logical Operators

```javascript
// Logical operators: &&, ||, !
let a = true;
let b = false;

console.log(a && b);    // false
console.log(a || b);    // true
console.log(!a);         // false

// Short-circuit evaluation
let name = null;
let displayName = name || "Anonymous";  // "Anonymous"
console.log(displayName);

// Nullish coalescing (??) - only checks null/undefined (ES2020+)
let value = 0;
console.log(value || "default");   // "default" (0 is falsy)
console.log(value ?? "default");   // 0 (0 is not null/undefined)

// Optional chaining (?.) - safe property access (ES2020+)
let user = { address: { city: "NYC" } };
console.log(user?.address?.city);    // "NYC"
console.log(user?.phone?.number);    // undefined (no error)

// Practical example
let age = 20;
let hasLicense = true;
let canDrive = age >= 18 && hasLicense;
console.log("Can drive:", canDrive);  // true
```

---

## Input and Output

### Console Output

```javascript
// Different console methods
console.log("Regular message");
console.warn("Warning message");
console.error("Error message");
console.info("Info message");

// Formatting
let name = "Alice";
let age = 25;
console.log(`Name: ${name}, Age: ${age}`);  // Template literal
console.log("Name:", name, "Age:", age);     // Multiple arguments

// Objects and arrays
console.log({ name: "Alice", age: 25 });
console.table([
    { name: "Alice", age: 25 },
    { name: "Bob", age: 30 }
]);

// Timing
console.time("loop");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("loop");  // loop: 2.345ms
```

### Browser Input

```javascript
// prompt - get string input from user (browser only)
let name = prompt("What's your name?");
console.log("Hello, " + name);

// confirm - get yes/no from user (browser only)
let proceed = confirm("Are you sure?");
console.log("User said:", proceed);  // true or false

// alert - show a message (browser only)
alert("Welcome to the site!");
```

### Node.js Input

```javascript
// Using readline module in Node.js
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("What's your name? ", (name) => {
    console.log(`Hello, ${name}!`);

    rl.question("How old are you? ", (age) => {
        console.log(`You are ${age} years old`);
        rl.close();
    });
});
```

---

## Conditional Statements

### if, else if, else

```javascript
// Basic if statement
let age = 18;

if (age >= 18) {
    console.log("You are an adult");
    console.log("You can vote");
}

// if-else
let temperature = 25;

if (temperature > 30) {
    console.log("It's hot outside");
} else {
    console.log("It's not too hot");
}

// if-else if-else
let score = 85;
let grade;

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

console.log(`Your grade is: ${grade}`);
```

### switch Statements

```javascript
// Traditional switch
let dayNumber = 3;
let dayName;

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
    case 7:
        dayName = "Weekend";
        break;
    default:
        dayName = "Invalid day";
}

console.log(`Day ${dayNumber} is ${dayName}`);

// Switch with strings
let command = "start";
switch (command) {
    case "start":
        console.log("Starting...");
        break;
    case "stop":
        console.log("Stopping...");
        break;
    default:
        console.log("Unknown command");
}
```

### Ternary and Short-Circuit Patterns

```javascript
// Ternary operator
let age = 20;
let status = age >= 18 ? "Adult" : "Minor";
console.log(`Status: ${status}`);

// Nested ternary (use sparingly)
let score = 85;
let grade = score >= 90 ? "A" : score >= 80 ? "B" : "C or below";
console.log(`Grade: ${grade}`);

// Short-circuit patterns
let user = { name: "Alice" };
let displayName = user && user.name;  // "Alice"
let fallback = null ?? "default";     // "default"
```

---

## Loops

### for Loops

```javascript
// Basic for loop
console.log("Counting to 5:");
for (let i = 1; i <= 5; i++) {
    console.log(`Count: ${i}`);
}

// Loop with different increment
console.log("\nEven numbers from 2 to 10:");
for (let i = 2; i <= 10; i += 2) {
    console.log(i);
}

// Counting backwards
console.log("\nCountdown:");
for (let i = 5; i >= 1; i--) {
    console.log(i);
}
console.log("Blast off!");
```

### for...of and for...in Loops

```javascript
// for...of - iterate over values (arrays, strings, iterables)
let fruits = ["apple", "banana", "cherry"];

console.log("Fruits:");
for (let fruit of fruits) {
    console.log(`- ${fruit}`);
}

// for...of with string
for (let char of "Hello") {
    console.log(char);
}

// for...of with entries (index + value)
for (let [index, fruit] of fruits.entries()) {
    console.log(`${index}: ${fruit}`);
}

// for...in - iterate over object keys (properties)
let person = { name: "Alice", age: 25, city: "NYC" };

console.log("\nPerson properties:");
for (let key in person) {
    console.log(`${key}: ${person[key]}`);
}

// WARNING: Don't use for...in with arrays (use for...of instead)
```

### while and do-while Loops

```javascript
// Basic while loop
let count = 0;
while (count < 3) {
    console.log(`Count is: ${count}`);
    count++;
}

// do-while loop (executes at least once)
let input;
do {
    input = prompt("Enter 'quit' to exit:");
    console.log(`You entered: ${input}`);
} while (input !== "quit");

console.log("Goodbye!");
```

### Loop Control

```javascript
// break: Exit loop immediately
console.log("Numbers with break:");
for (let i = 0; i < 10; i++) {
    if (i === 5) break;
    console.log(i);  // Prints 0, 1, 2, 3, 4
}

// continue: Skip rest of current iteration
console.log("\nSkip multiples of 3:");
for (let i = 0; i < 10; i++) {
    if (i % 3 === 0) continue;
    console.log(i);  // Prints 1, 2, 4, 5, 7, 8
}

// Labeled break (break out of nested loops)
outer:
for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
        if (i === 1 && j === 1) break outer;
        console.log(`i=${i}, j=${j}`);
    }
}
```

---

## Functions

### Function Declarations and Expressions

```javascript
// Function declaration (hoisted - can be called before defined)
function sayHello() {
    console.log("Hello from a function!");
}

// Function with parameters and return value
function addNumbers(a, b) {
    return a + b;
}

// Function expression (not hoisted)
const greet = function(name) {
    console.log(`Hello, ${name}!`);
};

// Calling functions
sayHello();
greet("Alice");
let sum = addNumbers(5, 3);
console.log(`5 + 3 = ${sum}`);
```

### Arrow Functions

```javascript
// Arrow function (concise syntax, ES2015+)
const add = (a, b) => a + b;
const square = x => x * x;        // Single param: no parens needed
const doNothing = () => {};        // No params: empty parens

console.log(add(5, 3));    // 8
console.log(square(4));    // 16

// Multi-line arrow function
const calculateArea = (length, width) => {
    let area = length * width;
    return area;
};

console.log(`Area: ${calculateArea(4.5, 6.2)}`);

// Arrow functions and 'this' (arrow functions don't bind their own 'this')
const obj = {
    name: "Alice",
    // Regular function: 'this' refers to obj
    greetRegular: function() {
        console.log(`Hello, ${this.name}`);
    },
    // Arrow function: 'this' is inherited from enclosing scope
    greetArrow: () => {
        console.log(`Hello, ${this.name}`);  // 'this' is NOT obj
    }
};
```

### Default Parameters and Rest/Spread

```javascript
// Default parameters
function greet(name, greeting = "Hello") {
    console.log(`${greeting}, ${name}!`);
}

greet("Alice");          // "Hello, Alice!"
greet("Bob", "Hi");     // "Hi, Bob!"

// Rest parameters (...args collects remaining arguments)
function sumAll(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}

console.log(sumAll(1, 2, 3));        // 6
console.log(sumAll(1, 2, 3, 4, 5));  // 15

// Spread operator (expands an array)
let nums = [1, 2, 3];
console.log(Math.max(...nums));  // 3

let moreNums = [0, ...nums, 4, 5];
console.log(moreNums);  // [0, 1, 2, 3, 4, 5]
```

### Closures and Higher-Order Functions

```javascript
// Closure: function that remembers its outer scope
function createCounter() {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

let counter = createCounter();
console.log(counter.increment());  // 1
console.log(counter.increment());  // 2
console.log(counter.decrement());  // 1
console.log(counter.getCount());   // 1

// Higher-order functions (functions that take/return functions)
function applyOperation(a, b, operation) {
    return operation(a, b);
}

console.log(applyOperation(5, 3, (a, b) => a + b));  // 8
console.log(applyOperation(5, 3, (a, b) => a * b));  // 15
```

---

## Arrays

### Array Basics

```javascript
// Creating arrays
let numbers = [1, 2, 3, 4, 5];
let fruits = ["apple", "banana", "cherry"];
let mixed = [1, "hello", true, null, { key: "value" }];
let empty = [];
let filled = new Array(5).fill(0);  // [0, 0, 0, 0, 0]

// Accessing elements (0-indexed)
console.log(fruits[0]);          // "apple"
console.log(fruits[fruits.length - 1]); // "cherry"
console.log(fruits.at(-1));      // "cherry" (ES2022+)

// Modifying elements
fruits[1] = "blueberry";
console.log(fruits);  // ["apple", "blueberry", "cherry"]

// Array length
console.log(fruits.length);  // 3
```

### Array Methods - Mutating

```javascript
let arr = [1, 2, 3];

// push / pop - add/remove from end
arr.push(4);           // [1, 2, 3, 4]
let popped = arr.pop(); // [1, 2, 3], popped = 4

// unshift / shift - add/remove from beginning
arr.unshift(0);         // [0, 1, 2, 3]
let shifted = arr.shift(); // [1, 2, 3], shifted = 0

// splice - add/remove at any position
arr.splice(1, 1);         // Remove 1 element at index 1: [1, 3]
arr.splice(1, 0, 2);      // Insert 2 at index 1: [1, 2, 3]
arr.splice(1, 1, 20, 30); // Replace 1 element at index 1: [1, 20, 30, 3]

// sort and reverse
let names = ["Charlie", "Alice", "Bob"];
names.sort();      // ["Alice", "Bob", "Charlie"]
names.reverse();   // ["Charlie", "Bob", "Alice"]

// Numeric sort (need a compare function!)
let nums = [10, 1, 21, 2];
nums.sort((a, b) => a - b);  // [1, 2, 10, 21]
```

### Array Methods - Non-Mutating

```javascript
let numbers = [1, 2, 3, 4, 5];

// map - transform each element
let doubled = numbers.map(n => n * 2);
console.log(doubled);  // [2, 4, 6, 8, 10]

// filter - keep elements that pass a test
let evens = numbers.filter(n => n % 2 === 0);
console.log(evens);  // [2, 4]

// reduce - accumulate to a single value
let sum = numbers.reduce((total, n) => total + n, 0);
console.log(sum);  // 15

// find - first element that passes test
let found = numbers.find(n => n > 3);
console.log(found);  // 4

// findIndex - index of first match
let index = numbers.findIndex(n => n > 3);
console.log(index);  // 3

// some / every - test conditions
console.log(numbers.some(n => n > 4));   // true (at least one)
console.log(numbers.every(n => n > 0));  // true (all pass)

// includes - check if element exists
console.log(numbers.includes(3));  // true

// slice - extract a portion (non-mutating)
let middle = numbers.slice(1, 4);  // [2, 3, 4]
let last2 = numbers.slice(-2);     // [4, 5]

// concat - merge arrays
let more = numbers.concat([6, 7, 8]);
console.log(more);  // [1, 2, 3, 4, 5, 6, 7, 8]

// flat - flatten nested arrays
let nested = [[1, 2], [3, [4, 5]]];
console.log(nested.flat());    // [1, 2, 3, [4, 5]]
console.log(nested.flat(2));   // [1, 2, 3, 4, 5]

// join - convert to string
console.log(["a", "b", "c"].join(", "));  // "a, b, c"
```

### Destructuring Arrays

```javascript
// Array destructuring
let [first, second, third] = ["apple", "banana", "cherry"];
console.log(first);   // "apple"
console.log(second);  // "banana"

// Skip elements
let [a, , c] = [1, 2, 3];
console.log(a, c);  // 1 3

// Rest pattern
let [head, ...tail] = [1, 2, 3, 4, 5];
console.log(head);  // 1
console.log(tail);  // [2, 3, 4, 5]

// Swap variables
let x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y);  // 2 1
```

---

## Objects

### Object Basics

```javascript
// Creating objects
let person = {
    name: "Alice",
    age: 25,
    city: "New York",
    isStudent: true
};

// Accessing properties
console.log(person.name);         // Dot notation
console.log(person["age"]);       // Bracket notation
console.log(person.nonexistent);  // undefined

// Modifying properties
person.age = 26;
person.email = "alice@example.com";  // Add new property
delete person.isStudent;              // Remove property

// Check if property exists
console.log("name" in person);          // true
console.log(person.hasOwnProperty("age")); // true
```

### Object Methods and 'this'

```javascript
let calculator = {
    result: 0,

    add(value) {
        this.result += value;
        return this;  // Enable chaining
    },

    subtract(value) {
        this.result -= value;
        return this;
    },

    getResult() {
        return this.result;
    }
};

// Method chaining
calculator.add(10).subtract(3).add(5);
console.log(calculator.getResult());  // 12
```

### Object Destructuring

```javascript
let person = { name: "Alice", age: 25, city: "NYC" };

// Basic destructuring
let { name, age } = person;
console.log(name, age);  // "Alice" 25

// Rename variables
let { name: fullName, age: years } = person;
console.log(fullName, years);  // "Alice" 25

// Default values
let { name: n, country = "USA" } = person;
console.log(n, country);  // "Alice" "USA"

// Rest pattern
let { name: personName, ...rest } = person;
console.log(personName);  // "Alice"
console.log(rest);         // { age: 25, city: "NYC" }

// Nested destructuring
let user = {
    id: 1,
    address: { city: "NYC", zip: "10001" }
};
let { address: { city, zip } } = user;
console.log(city, zip);  // "NYC" "10001"
```

### Spread and Useful Patterns

```javascript
// Spread operator with objects
let defaults = { theme: "light", lang: "en", fontSize: 14 };
let userPrefs = { theme: "dark", fontSize: 16 };
let settings = { ...defaults, ...userPrefs };
console.log(settings);
// { theme: "dark", lang: "en", fontSize: 16 }

// Object.keys, values, entries
let person = { name: "Alice", age: 25, city: "NYC" };
console.log(Object.keys(person));    // ["name", "age", "city"]
console.log(Object.values(person));  // ["Alice", 25, "NYC"]
console.log(Object.entries(person)); // [["name","Alice"], ["age",25], ["city","NYC"]]

// Object.freeze (prevent modifications)
let config = Object.freeze({ port: 3000, host: "localhost" });
config.port = 8080;  // Silently fails (or throws in strict mode)
console.log(config.port);  // 3000

// Computed property names
let key = "color";
let obj = { [key]: "blue", [`${key}Code`]: "#0000FF" };
console.log(obj);  // { color: "blue", colorCode: "#0000FF" }
```

### Maps and Sets

```javascript
// Map - key-value pairs (any type as key)
let map = new Map();
map.set("name", "Alice");
map.set(42, "a number key");
map.set(true, "a boolean key");

console.log(map.get("name"));  // "Alice"
console.log(map.size);          // 3
console.log(map.has("name"));   // true

map.delete(42);

for (let [key, value] of map) {
    console.log(`${key}: ${value}`);
}

// Set - unique values only
let set = new Set([1, 2, 3, 3, 4, 4, 5]);
console.log(set);       // Set { 1, 2, 3, 4, 5 }
console.log(set.size);  // 5

set.add(6);
set.delete(1);
console.log(set.has(3));  // true

// Remove duplicates from array
let arr = [1, 2, 2, 3, 3, 4];
let unique = [...new Set(arr)];
console.log(unique);  // [1, 2, 3, 4]
```

---

## String Manipulation

### String Basics

```javascript
let text = "Hello, World!";

// Properties and methods
console.log(text.length);          // 13
console.log(text.toUpperCase());   // "HELLO, WORLD!"
console.log(text.toLowerCase());   // "hello, world!"

// Checking
console.log(text.startsWith("Hello"));  // true
console.log(text.endsWith("!"));        // true
console.log(text.includes("World"));    // true

// Accessing characters
console.log(text[0]);              // "H"
console.log(text.charAt(0));       // "H"
console.log(text.at(-1));          // "!" (ES2022+)

// Finding substrings
console.log(text.indexOf("World"));     // 7
console.log(text.lastIndexOf("l"));     // 10
console.log(text.search(/world/i));     // 7 (regex search)
```

### String Manipulation Methods

```javascript
// Substring extraction
let text = "Hello, World!";
console.log(text.slice(0, 5));     // "Hello"
console.log(text.slice(7));        // "World!"
console.log(text.slice(-6));       // "orld!"
console.log(text.substring(0, 5)); // "Hello"

// Replacing
console.log(text.replace("World", "JavaScript"));  // "Hello, JavaScript!"
console.log("aabbcc".replace(/(.)\1/g, "$1"));      // "abc" (regex)
console.log("hello".replaceAll("l", "L"));           // "heLLo"

// Splitting and joining
let csv = "apple,banana,cherry,date";
let parts = csv.split(",");
console.log(parts);  // ["apple", "banana", "cherry", "date"]

let joined = parts.join(" | ");
console.log(joined);  // "apple | banana | cherry | date"

// Trimming
let padded = "  Hello, World!  ";
console.log(padded.trim());       // "Hello, World!"
console.log(padded.trimStart());  // "Hello, World!  "
console.log(padded.trimEnd());    // "  Hello, World!"

// Padding
console.log("5".padStart(3, "0"));   // "005"
console.log("Hi".padEnd(10, "."));   // "Hi........"

// Repeating
console.log("ha".repeat(3));  // "hahaha"
```

### Template Literals

```javascript
let name = "Alice";
let age = 25;

// String interpolation
let greeting = `Hello, ${name}! You are ${age} years old.`;
console.log(greeting);

// Expressions in templates
console.log(`2 + 3 = ${2 + 3}`);
console.log(`Is adult: ${age >= 18 ? "Yes" : "No"}`);

// Multi-line strings
let html = `
<div class="card">
    <h2>${name}</h2>
    <p>Age: ${age}</p>
</div>
`;
console.log(html);

// Tagged templates (advanced)
function highlight(strings, ...values) {
    return strings.reduce((result, str, i) => {
        return result + str + (values[i] ? `**${values[i]}**` : "");
    }, "");
}

let result = highlight`Hello ${name}, you are ${age}`;
console.log(result);  // "Hello **Alice**, you are **25**"
```

---

## Error Handling

### Try-Catch

```javascript
// Basic try-catch
try {
    let result = 10 / 0;       // Infinity (no error in JS)
    console.log(result);

    JSON.parse("invalid json");  // Throws SyntaxError
} catch (error) {
    console.log("Error caught:", error.message);
    console.log("Error type:", error.name);
}

// try-catch-finally
try {
    let data = JSON.parse('{"name": "Alice"}');
    console.log(data.name);
} catch (error) {
    console.log("Parse error:", error.message);
} finally {
    console.log("This always runs");
}

// Catching specific error types
try {
    undeclaredVariable;
} catch (error) {
    if (error instanceof ReferenceError) {
        console.log("Reference error:", error.message);
    } else if (error instanceof TypeError) {
        console.log("Type error:", error.message);
    } else {
        throw error;  // Re-throw unknown errors
    }
}
```

### Throwing Errors

```javascript
// Throwing custom errors
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    console.log(divide(10, 0));
} catch (error) {
    console.log("Caught:", error.message);
}

// Custom error class
class ValidationError extends Error {
    constructor(field, message) {
        super(message);
        this.name = "ValidationError";
        this.field = field;
    }
}

function validateAge(age) {
    if (typeof age !== "number") {
        throw new ValidationError("age", "Age must be a number");
    }
    if (age < 0 || age > 150) {
        throw new ValidationError("age", "Age must be between 0 and 150");
    }
    return true;
}

try {
    validateAge("twenty");
} catch (error) {
    if (error instanceof ValidationError) {
        console.log(`${error.field}: ${error.message}`);
    }
}
```

---

## DOM Manipulation

### Selecting Elements

```javascript
// By ID
let header = document.getElementById("main-header");

// By CSS selector (first match)
let firstButton = document.querySelector(".btn");
let nav = document.querySelector("nav > ul");

// By CSS selector (all matches)
let allButtons = document.querySelectorAll(".btn");
let listItems = document.querySelectorAll("li");

// By class name / tag name
let cards = document.getElementsByClassName("card");
let paragraphs = document.getElementsByTagName("p");

// Iterate over NodeList
allButtons.forEach(button => {
    console.log(button.textContent);
});
```

### Modifying Elements

```javascript
// Text content
let heading = document.querySelector("h1");
heading.textContent = "New Heading";      // Plain text
heading.innerHTML = "<em>New</em> Heading"; // HTML content

// Attributes
let link = document.querySelector("a");
link.setAttribute("href", "https://example.com");
link.getAttribute("href");
link.removeAttribute("target");

// CSS styles
let box = document.querySelector(".box");
box.style.backgroundColor = "blue";
box.style.padding = "20px";
box.style.borderRadius = "8px";

// CSS classes
box.classList.add("active");
box.classList.remove("hidden");
box.classList.toggle("highlighted");
console.log(box.classList.contains("active"));  // true
```

### Creating and Removing Elements

```javascript
// Create new element
let newDiv = document.createElement("div");
newDiv.textContent = "I'm new!";
newDiv.classList.add("card");

// Append to parent
let container = document.querySelector("#container");
container.appendChild(newDiv);

// Insert before another element
let reference = document.querySelector("#reference");
container.insertBefore(newDiv, reference);

// Remove element
let oldElement = document.querySelector(".old");
oldElement.remove();  // Modern way
// oldElement.parentNode.removeChild(oldElement);  // Older way
```

### Event Handling

```javascript
// Add event listener
let button = document.querySelector("#myButton");

button.addEventListener("click", function(event) {
    console.log("Button clicked!");
    console.log("Target:", event.target);
});

// Arrow function listener
button.addEventListener("click", (e) => {
    e.preventDefault();  // Prevent default behavior
    console.log("Clicked at:", e.clientX, e.clientY);
});

// Common events: click, submit, keydown, keyup, mouseover,
//                mouseout, change, input, load, DOMContentLoaded

// Event delegation (handle events on dynamic children)
let list = document.querySelector("#todo-list");
list.addEventListener("click", (e) => {
    if (e.target.tagName === "LI") {
        e.target.classList.toggle("completed");
    }
});

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM is ready");
});
```

---

## Asynchronous JavaScript

### Callbacks

```javascript
// setTimeout / setInterval
console.log("Start");

setTimeout(() => {
    console.log("After 2 seconds");
}, 2000);

console.log("End");
// Output: "Start", "End", "After 2 seconds"

// setInterval (repeating)
let count = 0;
let intervalId = setInterval(() => {
    count++;
    console.log(`Tick ${count}`);
    if (count >= 3) {
        clearInterval(intervalId);
    }
}, 1000);
```

### Promises

```javascript
// Creating a promise
function fetchData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url) {
                resolve({ data: "Some data from " + url });
            } else {
                reject(new Error("URL is required"));
            }
        }, 1000);
    });
}

// Using promises with .then/.catch
fetchData("https://api.example.com")
    .then(result => {
        console.log("Success:", result.data);
        return result.data.toUpperCase();
    })
    .then(upper => {
        console.log("Uppercased:", upper);
    })
    .catch(error => {
        console.log("Error:", error.message);
    })
    .finally(() => {
        console.log("Done");
    });

// Promise.all - wait for all to complete
let p1 = fetchData("/api/users");
let p2 = fetchData("/api/posts");

Promise.all([p1, p2])
    .then(([users, posts]) => {
        console.log(users, posts);
    })
    .catch(error => console.log(error));

// Promise.race - first to complete
Promise.race([p1, p2])
    .then(first => console.log("First:", first));
```

### Async/Await

```javascript
// async/await - cleaner syntax for promises
async function loadData() {
    try {
        let response = await fetch("https://jsonplaceholder.typicode.com/todos/1");
        let data = await response.json();
        console.log("Todo:", data.title);
        return data;
    } catch (error) {
        console.log("Error:", error.message);
    }
}

loadData();

// Parallel async operations
async function loadAll() {
    try {
        let [users, posts] = await Promise.all([
            fetch("/api/users").then(r => r.json()),
            fetch("/api/posts").then(r => r.json())
        ]);
        console.log(users, posts);
    } catch (error) {
        console.log("Error:", error.message);
    }
}

// Async arrow function
const getData = async () => {
    let response = await fetch("/api/data");
    return response.json();
};

// Top-level await (ES2022+ modules)
// let data = await fetch("/api/data");
```

---

## Modules

### ES Modules (Modern)

**math.js:**
```javascript
// Named exports
export function add(a, b) {
    return a + b;
}

export function subtract(a, b) {
    return a - b;
}

export const PI = 3.14159;

// Default export (one per module)
export default function multiply(a, b) {
    return a * b;
}
```

**main.js:**
```javascript
// Import named exports
import { add, subtract, PI } from "./math.js";

// Import default export
import multiply from "./math.js";

// Import all as namespace
import * as math from "./math.js";

console.log(add(5, 3));        // 8
console.log(multiply(4, 2));   // 8
console.log(math.PI);          // 3.14159

// Rename imports
import { add as sum } from "./math.js";
console.log(sum(1, 2));  // 3
```

### CommonJS (Node.js)

**utils.js:**
```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

function farewell(name) {
    return `Goodbye, ${name}!`;
}

module.exports = { greet, farewell };
```

**app.js:**
```javascript
const { greet, farewell } = require("./utils");

console.log(greet("Alice"));
console.log(farewell("Bob"));
```

---

## Practice Exercises

### Exercise 1: Temperature Converter

```javascript
function celsiusToFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

function fahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

// Test
console.log(`0°C = ${celsiusToFahrenheit(0)}°F`);     // 32
console.log(`100°C = ${celsiusToFahrenheit(100)}°F`);  // 212
console.log(`72°F = ${fahrenheitToCelsius(72).toFixed(1)}°C`);  // 22.2
```

### Exercise 2: Array Statistics

```javascript
function arrayStats(arr) {
    if (arr.length === 0) return null;

    let sorted = [...arr].sort((a, b) => a - b);
    let sum = arr.reduce((total, n) => total + n, 0);
    let mean = sum / arr.length;

    let mid = Math.floor(arr.length / 2);
    let median = arr.length % 2 !== 0
        ? sorted[mid]
        : (sorted[mid - 1] + sorted[mid]) / 2;

    return {
        min: sorted[0],
        max: sorted[sorted.length - 1],
        sum: sum,
        mean: mean,
        median: median,
        count: arr.length
    };
}

let data = [4, 2, 7, 1, 9, 3, 5, 8, 6];
let stats = arrayStats(data);
console.log("Stats:", stats);
```

### Exercise 3: Todo List

```javascript
class TodoList {
    constructor() {
        this.todos = [];
        this.nextId = 1;
    }

    add(text) {
        let todo = { id: this.nextId++, text, completed: false };
        this.todos.push(todo);
        return todo;
    }

    toggle(id) {
        let todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
        }
        return todo;
    }

    remove(id) {
        this.todos = this.todos.filter(t => t.id !== id);
    }

    list(showAll = true) {
        let items = showAll
            ? this.todos
            : this.todos.filter(t => !t.completed);

        items.forEach(t => {
            let status = t.completed ? "[x]" : "[ ]";
            console.log(`${status} ${t.id}. ${t.text}`);
        });
    }
}

let todos = new TodoList();
todos.add("Learn JavaScript");
todos.add("Build a project");
todos.add("Read documentation");
todos.toggle(1);
todos.list();
// [x] 1. Learn JavaScript
// [ ] 2. Build a project
// [ ] 3. Read documentation
```

### Exercise 4: Simple Fetch Wrapper

```javascript
async function api(baseUrl) {
    async function request(method, path, body = null) {
        let options = {
            method,
            headers: { "Content-Type": "application/json" }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        let response = await fetch(`${baseUrl}${path}`, options);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return response.json();
    }

    return {
        get: (path) => request("GET", path),
        post: (path, body) => request("POST", path, body),
        put: (path, body) => request("PUT", path, body),
        delete: (path) => request("DELETE", path)
    };
}

// Usage
async function demo() {
    let client = api("https://jsonplaceholder.typicode.com");

    let todo = await client.get("/todos/1");
    console.log("Todo:", todo.title);

    let newPost = await client.post("/posts", {
        title: "My Post",
        body: "Content here",
        userId: 1
    });
    console.log("Created:", newPost);
}

demo().catch(console.error);
```

---

## Summary

These notes cover the fundamental concepts of JavaScript:

1. **Variables and Types**: `let`, `const`, `var`; primitives (number, string, boolean, null, undefined, symbol, bigint); type coercion
2. **Operations**: Arithmetic, comparison (`===` preferred), logical, nullish coalescing (`??`), optional chaining (`?.`)
3. **Functions**: Declarations, expressions, arrow functions, closures, higher-order functions, rest/spread
4. **Arrays**: Mutating methods (push, pop, splice, sort), non-mutating methods (map, filter, reduce, find), destructuring
5. **Objects**: Properties, methods, destructuring, spread, Maps, Sets
6. **Control Flow**: if/else, switch, ternary, for/for...of/for...in, while, break/continue
7. **Error Handling**: try/catch/finally, throwing custom errors
8. **DOM**: Selecting, modifying, creating elements; event handling and delegation
9. **Async**: Callbacks, Promises, async/await, fetch API
10. **Modules**: ES modules (import/export), CommonJS (require)

### Next Steps

1. Practice the exercises and build small projects
2. Learn about classes and prototypal inheritance in depth
3. Explore Node.js for server-side JavaScript
4. Study popular frameworks (React, Vue, or Angular)
5. Learn TypeScript for type-safe JavaScript development

### Additional Resources

- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **JavaScript.info**: https://javascript.info/
- **Node.js Documentation**: https://nodejs.org/en/docs/
- **ECMAScript Specification**: https://tc39.es/ecma262/
- **Practice Problems**: https://exercism.org/tracks/javascript
