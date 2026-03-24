# Elementary Ruby Programming Concepts

## Table of Contents

1. [Getting Started with Ruby](#getting-started-with-ruby)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops and Iterators](#loops-and-iterators)
7. [Methods](#methods)
8. [Arrays](#arrays)
9. [Hashes](#hashes)
10. [String Manipulation](#string-manipulation)
11. [Blocks, Procs, and Lambdas](#blocks-procs-and-lambdas)
12. [Error Handling](#error-handling)
13. [File Operations](#file-operations)
14. [Classes and Objects](#classes-and-objects)
15. [Practice Exercises](#practice-exercises)
16. [Summary](#summary)

---

## Getting Started with Ruby

### What is Ruby?

Ruby is a dynamic, object-oriented programming language designed for simplicity and productivity. Key features:
- **Everything is an object**: Even numbers and booleans are objects with methods
- **Dynamically typed**: Variable types are determined at runtime
- **Expressive syntax**: Designed to read like natural English
- **Duck typing**: "If it walks like a duck and quacks like a duck, it's a duck"
- **Convention over configuration**: Emphasized by frameworks like Rails
- **Garbage collected**: Automatic memory management

### Your First Ruby Program

```ruby
# This is a comment
puts "Hello, World!"
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **puts** - Prints a string with a newline at the end
- **print** - Prints without a newline
- **p** - Prints the `.inspect` representation (useful for debugging)
- **#** - Single-line comment
- **=begin ... =end** - Multi-line comment (must start at beginning of line)
- No semicolons needed (newlines end statements)
- No `main` function — code runs top to bottom

### Development Environment

- **Ruby**: Install via rbenv, rvm, or system package manager
- **IRB (Interactive Ruby)**: Built-in REPL for experimenting
- **RubyGems**: Package manager (bundled with Ruby)
- **Bundler**: Dependency manager using a Gemfile
- **VS Code / RubyMine**: Popular editors and IDEs

### Running Ruby

```bash
ruby hello.rb          # Run a Ruby script
irb                    # Start interactive Ruby shell
ruby -e 'puts "Hi"'   # Run inline code
gem install rails      # Install a gem (package)
```

---

## Variables and Data Types

### Variable Types

```ruby
# Local variable (lowercase or underscore start)
name = "Alice"
age = 25
is_student = true

# Constants (uppercase start, convention: ALL_CAPS)
PI = 3.14159
MAX_SIZE = 100
# PI = 3.14  # Warning: already initialized constant

# Instance variable (belongs to an object)
@name = "Alice"

# Class variable (shared across all instances)
@@count = 0

# Global variable (avoid using these)
$debug_mode = false

puts name     # "Alice"
puts age      # 25
```

### Data Types

```ruby
# 1. Integer
integer = 42
big_num = 1_000_000      # Underscores for readability
hex = 0xFF                # 255
binary = 0b1010           # 10

puts integer.class        # Integer

# 2. Float
pi = 3.14
scientific = 2.5e3        # 2500.0

puts pi.class             # Float

# 3. String
single = 'Hello'          # No interpolation
double = "Hello, #{name}" # Interpolation with #{}
multi = <<~HEREDOC
  This is a
  multi-line string
HEREDOC

puts double               # "Hello, Alice"

# 4. Symbol (immutable, memory-efficient identifiers)
status = :active
role = :admin

puts status.class         # Symbol
puts :active == :active   # true (same object in memory)

# 5. Boolean
is_valid = true
is_empty = false

# 6. Nil (absence of value)
nothing = nil
puts nothing.nil?         # true
puts nothing.class        # NilClass

# 7. Array
fruits = ["apple", "banana", "cherry"]

# 8. Hash (key-value pairs)
person = { name: "Alice", age: 25 }

# Type checking
puts 42.is_a?(Integer)     # true
puts "hello".is_a?(String) # true
puts nil.is_a?(NilClass)   # true
puts 42.respond_to?(:+)    # true (can it respond to + method?)
```

### Type Conversion

```ruby
# Converting between types
puts "42".to_i           # 42 (string to integer)
puts "3.14".to_f         # 3.14 (string to float)
puts 42.to_s             # "42" (integer to string)
puts 42.to_f             # 42.0 (integer to float)
puts 3.14.to_i           # 3 (float to integer, truncates)
puts nil.to_s            # "" (nil to string)
puts nil.to_i            # 0 (nil to integer)
puts nil.to_a            # [] (nil to array)

# Integer methods
puts 42.even?            # true
puts 42.odd?             # false
puts -5.abs              # 5
puts 42.zero?            # false
```

---

## Basic Operations

### Arithmetic Operators

```ruby
a = 10
b = 3

puts a + b      # 13
puts a - b      # 7
puts a * b      # 30
puts a / b      # 3 (integer division)
puts a.to_f / b # 3.3333... (float division)
puts a % b      # 1 (modulus)
puts a ** b     # 1000 (exponentiation)

# Compound assignment
x = 5
x += 3    # 8
x -= 2    # 6
x *= 2    # 12
x /= 4   # 3
x %= 2   # 1
x **= 3  # 1

# Useful numeric methods
puts 10.gcd(6)           # 2 (greatest common divisor)
puts 10.lcm(6)           # 30 (least common multiple)
puts -5.abs              # 5
puts 3.14.round          # 3
puts 3.14.ceil           # 4
puts 3.14.floor          # 3
puts 5.between?(1, 10)   # true
```

### Comparison Operators

```ruby
x = 5
y = 10

puts x == y      # false
puts x != y      # true
puts x < y       # true
puts x > y       # false
puts x <= y      # true
puts x >= y      # false

# Spaceship operator (returns -1, 0, or 1)
puts 1 <=> 2     # -1
puts 2 <=> 2     # 0
puts 3 <=> 2     # 1

# equal? checks object identity (same object in memory)
a = "hello"
b = "hello"
puts a == b       # true (same value)
puts a.equal?(b)  # false (different objects)

# eql? checks type and value
puts 1 == 1.0     # true (coerces)
puts 1.eql?(1.0)  # false (different types)
```

### Logical Operators

```ruby
a = true
b = false

puts a && b      # false
puts a || b      # true
puts !a          # false

# and / or (lower precedence, use for control flow)
puts a and b     # false
puts a or b      # true

# Practical example
age = 20
has_license = true
can_drive = age >= 18 && has_license
puts "Can drive: #{can_drive}"
```

---

## Input and Output

### Output Methods

```ruby
# puts - print with newline
puts "Hello"
puts "World"
# Hello
# World

# print - print without newline
print "Hello "
print "World\n"
# Hello World

# p - debug output (shows inspect form)
p "Hello"        # "Hello"
p 42             # 42
p [1, 2, 3]      # [1, 2, 3]
p nil            # nil

# pp - pretty print (for complex objects)
pp({ name: "Alice", scores: [95, 87, 92] })

# printf / sprintf
printf("Name: %s, Age: %d, GPA: %.2f\n", "Alice", 25, 3.85)
formatted = sprintf("Price: $%.2f", 19.99)
puts formatted
```

### Getting User Input

```ruby
# gets reads a line from standard input (includes newline)
print "What's your name? "
name = gets.chomp  # chomp removes trailing newline

print "How old are you? "
age = gets.chomp.to_i

print "What's your height? "
height = gets.chomp.to_f

puts "Hello, #{name}! You are #{age} years old and #{height}m tall."
```

---

## Conditional Statements

### if, elsif, else

```ruby
# Basic if
age = 18

if age >= 18
  puts "You are an adult"
  puts "You can vote"
end

# if-else
temperature = 25

if temperature > 30
  puts "It's hot outside"
else
  puts "It's not too hot"
end

# if-elsif-else
score = 85

grade = if score >= 90
          "A"
        elsif score >= 80
          "B"
        elsif score >= 70
          "C"
        elsif score >= 60
          "D"
        else
          "F"
        end

puts "Your grade is: #{grade}"

# Inline if (modifier form)
puts "Adult" if age >= 18

# unless (opposite of if)
puts "You can enter" unless age < 18
```

### case Statements

```ruby
# case/when (Ruby's switch)
day_number = 3

day_name = case day_number
           when 1 then "Monday"
           when 2 then "Tuesday"
           when 3 then "Wednesday"
           when 4 then "Thursday"
           when 5 then "Friday"
           when 6, 7 then "Weekend"
           else "Invalid day"
           end

puts "Day #{day_number} is #{day_name}"

# case with ranges
age = 25
category = case age
           when 0..12 then "Child"
           when 13..17 then "Teenager"
           when 18..64 then "Adult"
           when 65.. then "Senior"
           else "Invalid age"
           end

puts "Category: #{category}"

# case with regex
input = "hello@example.com"
result = case input
         when /\A[\w.]+@[\w.]+\z/
           "Looks like an email"
         when /\A\d+\z/
           "Looks like a number"
         else
           "Unknown format"
         end

puts result

# case with classes
value = 42
case value
when Integer then puts "It's an integer"
when String then puts "It's a string"
when Array then puts "It's an array"
end

# Pattern matching (Ruby 3.0+)
data = { name: "Alice", age: 25 }

case data
in { name: String => name, age: (18..) => age }
  puts "#{name} is an adult (#{age})"
in { name: String => name, age: Integer => age }
  puts "#{name} is a minor (#{age})"
end
```

### Ternary Operator

```ruby
age = 20

# Ternary
status = age >= 18 ? "Adult" : "Minor"
puts "Status: #{status}"

# Practical example
x = 10
y = 20
max = x > y ? x : y
puts "Maximum: #{max}"
```

---

## Loops and Iterators

### Times, Upto, Downto

```ruby
# times - repeat n times
5.times do |i|
  puts "Count: #{i}"  # 0 to 4
end

# upto
1.upto(5) { |i| puts i }   # 1 to 5

# downto
5.downto(1) { |i| puts i } # 5 to 1
puts "Blast off!"

# step
1.step(10, 2) { |i| print "#{i} " }  # 1 3 5 7 9
puts
```

### Each and Iterators

```ruby
# each - the Ruby way to iterate
fruits = ["apple", "banana", "cherry"]

fruits.each do |fruit|
  puts "- #{fruit}"
end

# each with index
fruits.each_with_index do |fruit, i|
  puts "#{i + 1}. #{fruit}"
end

# each on a range
(1..5).each { |n| print "#{n} " }
puts

# each on a hash
person = { name: "Alice", age: 25, city: "NYC" }
person.each do |key, value|
  puts "#{key}: #{value}"
end

# map / collect - transform elements
numbers = [1, 2, 3, 4, 5]
doubled = numbers.map { |n| n * 2 }
puts doubled.inspect  # [2, 4, 6, 8, 10]

# select / filter - keep matching elements
evens = numbers.select { |n| n.even? }
puts evens.inspect  # [2, 4]

# reject - remove matching elements
odds = numbers.reject { |n| n.even? }
puts odds.inspect  # [1, 3, 5]

# reduce / inject - accumulate
sum = numbers.reduce(0) { |total, n| total + n }
puts "Sum: #{sum}"  # 15

# Also works with symbol
sum = numbers.reduce(:+)
puts "Sum: #{sum}"  # 15
```

### while and until Loops

```ruby
# while loop
count = 0
while count < 3
  puts "Count: #{count}"
  count += 1
end

# until loop (opposite of while)
count = 0
until count >= 3
  puts "Count: #{count}"
  count += 1
end

# Modifier form
i = 0
i += 1 while i < 5
puts i  # 5

# loop with break
loop do
  print "Enter 'quit' to exit: "
  input = gets.chomp
  break if input == "quit"
  puts "You entered: #{input}"
end
```

### Loop Control

```ruby
# break - exit loop
(1..10).each do |i|
  break if i > 5
  puts i
end

# next - skip to next iteration (like continue)
(1..10).each do |i|
  next if i % 3 == 0
  print "#{i} "  # 1 2 4 5 7 8 10
end
puts

# redo - restart current iteration (rare)
# retry - restart the entire loop (rare)
```

---

## Methods

### Defining Methods

```ruby
# Basic method
def say_hello
  puts "Hello from a method!"
end

# Method with parameters
def greet(name)
  puts "Hello, #{name}!"
end

# Method with return value (last expression is returned)
def add(a, b)
  a + b  # Implicit return
end

# Explicit return
def divide(a, b)
  return "Cannot divide by zero" if b == 0
  a.to_f / b
end

# Calling methods
say_hello
greet("Alice")
puts "5 + 3 = #{add(5, 3)}"
puts "10 / 3 = #{divide(10, 3)}"
puts divide(10, 0)
```

### Default Parameters and Keyword Arguments

```ruby
# Default parameters
def greet(name, greeting = "Hello")
  puts "#{greeting}, #{name}!"
end

greet("Alice")          # "Hello, Alice!"
greet("Bob", "Hi")     # "Hi, Bob!"

# Keyword arguments
def create_user(name:, age:, role: "user")
  puts "Name: #{name}, Age: #{age}, Role: #{role}"
end

create_user(name: "Alice", age: 25)
create_user(age: 30, name: "Bob", role: "admin")

# Splat operator (*) - variable arguments
def sum_all(*numbers)
  numbers.reduce(0, :+)
end

puts sum_all(1, 2, 3)        # 6
puts sum_all(1, 2, 3, 4, 5)  # 15

# Double splat (**) - variable keyword arguments
def print_info(**options)
  options.each { |key, value| puts "#{key}: #{value}" }
end

print_info(name: "Alice", age: 25, city: "NYC")
```

### Predicate and Bang Methods

```ruby
# Predicate methods (end with ?) return boolean
puts 42.even?          # true
puts 42.odd?           # false
puts nil.nil?          # true
puts "hello".empty?    # false
puts [].empty?         # true
puts "hello".include?("ell")  # true
puts 5.between?(1, 10)  # true

# Bang methods (end with !) modify in place
arr = [3, 1, 2]
arr.sort!              # Modifies arr in place
puts arr.inspect       # [1, 2, 3]

str = "hello"
str.upcase!            # Modifies str in place
puts str               # "HELLO"

# Non-bang returns a new object
str = "hello"
upper = str.upcase     # str is unchanged
puts str               # "hello"
puts upper             # "HELLO"
```

---

## Arrays

### Array Basics

```ruby
# Creating arrays
numbers = [1, 2, 3, 4, 5]
fruits = %w[apple banana cherry]   # Word array shorthand
mixed = [1, "hello", true, nil, [1, 2]]
empty = []
filled = Array.new(5, 0)           # [0, 0, 0, 0, 0]
range_arr = (1..5).to_a            # [1, 2, 3, 4, 5]

# Accessing elements
puts fruits[0]          # "apple"
puts fruits[-1]         # "cherry" (from end)
puts fruits.first       # "apple"
puts fruits.last        # "cherry"
puts fruits[1..2]       # ["banana", "cherry"]
puts fruits.length      # 3 (also: .size, .count)

# Modifying
fruits << "date"        # Append (also: .push)
fruits.push("elderberry")
fruits.unshift("avocado")  # Add to front
fruits.pop              # Remove from end
fruits.shift            # Remove from front
fruits.delete("banana") # Remove by value
fruits.delete_at(0)     # Remove by index
```

### Array Methods

```ruby
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sorting
puts numbers.sort.inspect                  # [1, 1, 2, 3, 4, 5, 6, 9]
puts numbers.sort { |a, b| b <=> a }.inspect  # Descending

# Searching
puts numbers.include?(5)     # true
puts numbers.index(4)        # 2 (first occurrence)
puts numbers.count(1)        # 2
puts numbers.min              # 1
puts numbers.max              # 9
puts numbers.sum              # 31
puts numbers.minmax.inspect   # [1, 9]

# Transforming
puts numbers.uniq.inspect              # Remove duplicates
puts numbers.flatten.inspect           # Flatten nested arrays
puts numbers.compact.inspect           # Remove nils
puts numbers.reverse.inspect           # Reverse
puts numbers.sample                    # Random element
puts numbers.shuffle.inspect           # Random order
puts numbers.take(3).inspect           # First 3 elements
puts numbers.drop(3).inspect           # All except first 3

# Combining
a = [1, 2, 3]
b = [3, 4, 5]
puts (a + b).inspect       # [1, 2, 3, 3, 4, 5]
puts (a | b).inspect       # [1, 2, 3, 4, 5] (union)
puts (a & b).inspect       # [3] (intersection)
puts (a - b).inspect       # [1, 2] (difference)

# zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
puts names.zip(ages).inspect
# [["Alice", 25], ["Bob", 30], ["Charlie", 35]]

# Chaining
result = (1..10)
  .select(&:even?)
  .map { |n| n ** 2 }
  .reject { |n| n > 50 }
puts result.inspect  # [4, 16, 36]
```

---

## Hashes

### Hash Basics

```ruby
# Creating hashes
person = { "name" => "Alice", "age" => 25 }   # String keys
person2 = { name: "Bob", age: 30 }             # Symbol keys (preferred)

# Accessing
puts person2[:name]         # "Bob"
puts person2[:nonexistent]  # nil
puts person2.fetch(:name)   # "Bob" (raises error if missing)
puts person2.fetch(:missing, "default")  # "default"

# Modifying
person2[:email] = "bob@example.com"
person2[:age] = 31
person2.delete(:email)

# Checking
puts person2.key?(:name)       # true (also: has_key?, include?)
puts person2.value?(31)        # true (also: has_value?)
puts person2.empty?            # false
puts person2.length            # 2 (also: .size)
```

### Hash Methods

```ruby
person = { name: "Alice", age: 25, city: "NYC" }

# Keys and values
puts person.keys.inspect     # [:name, :age, :city]
puts person.values.inspect   # ["Alice", 25, "NYC"]
puts person.to_a.inspect     # [[:name, "Alice"], [:age, 25], [:city, "NYC"]]

# Iterating
person.each do |key, value|
  puts "#{key}: #{value}"
end

person.each_key { |k| puts k }
person.each_value { |v| puts v }

# Transforming
upper = person.transform_values { |v| v.to_s.upcase }
puts upper.inspect  # {name: "ALICE", age: "25", city: "NYC"}

mapped = person.map { |k, v| [k, v.to_s] }.to_h
puts mapped.inspect

# Selecting and rejecting
adults = { alice: 25, bob: 17, charlie: 30 }
of_age = adults.select { |_, age| age >= 18 }
puts of_age.inspect  # {alice: 25, charlie: 30}

# Merging
defaults = { theme: "light", lang: "en", font_size: 14 }
user_prefs = { theme: "dark", font_size: 16 }
settings = defaults.merge(user_prefs)
puts settings.inspect
# {theme: "dark", lang: "en", font_size: 16}

# Dig (nested access)
data = { user: { address: { city: "NYC" } } }
puts data.dig(:user, :address, :city)    # "NYC"
puts data.dig(:user, :phone, :number)    # nil (no error)
```

---

## String Manipulation

### String Basics

```ruby
text = "Hello, World!"

# Properties and methods
puts text.length          # 13 (also: .size)
puts text.upcase          # "HELLO, WORLD!"
puts text.downcase        # "hello, world!"
puts text.capitalize      # "Hello, world!"
puts text.swapcase        # "hELLO, wORLD!"

# Checking
puts text.start_with?("Hello")  # true
puts text.end_with?("!")        # true
puts text.include?("World")    # true
puts text.empty?                # false
puts "  ".strip.empty?         # true

# Accessing characters
puts text[0]              # "H"
puts text[-1]             # "!"
puts text[0..4]           # "Hello"
puts text[7..]            # "World!"

# Finding
puts text.index("World")       # 7
puts text.count("l")           # 3
```

### String Manipulation Methods

```ruby
# Replacing
text = "Hello, World!"
puts text.sub("World", "Ruby")      # First occurrence
puts text.gsub("l", "L")            # All occurrences
puts text.delete("lo")              # "He, Wrd!"
puts text.squeeze("l")              # "Helo, World!"

# Trimming
padded = "  Hello, World!  "
puts padded.strip           # "Hello, World!"
puts padded.lstrip          # "Hello, World!  "
puts padded.rstrip          # "  Hello, World!"
puts "***Hello***".delete_prefix("***")  # "Hello***"
puts "***Hello***".delete_suffix("***")  # "***Hello"

# Splitting and joining
csv = "apple,banana,cherry,date"
parts = csv.split(",")
puts parts.inspect      # ["apple", "banana", "cherry", "date"]
puts parts.join(" | ")  # "apple | banana | cherry | date"

# Characters and lines
puts "hello".chars.inspect      # ["h", "e", "l", "l", "o"]
puts "line1\nline2".lines.inspect  # ["line1\n", "line2"]

# Padding and centering
puts "5".rjust(5, "0")     # "00005"
puts "Hi".ljust(10, ".")   # "Hi........"
puts "Hi".center(10, "-")  # "----Hi----"

# Repeating
puts "ha" * 3              # "hahaha"

# Reversing
puts "Hello".reverse       # "olleH"

# Encoding
puts "hello".encoding      # UTF-8
puts "hello".bytes.inspect # [104, 101, 108, 108, 111]
```

### String Interpolation and Formatting

```ruby
name = "Alice"
age = 25

# Interpolation (double quotes only)
puts "Hello, #{name}! You are #{age} years old."
puts "2 + 3 = #{2 + 3}"

# Format string
puts format("Name: %s, Age: %d, GPA: %.2f", name, age, 3.85)
puts "Price: $%0.2f" % 19.99

# Frozen strings (immutable)
frozen = "hello".freeze
# frozen << " world"  # RuntimeError: can't modify frozen String
```

---

## Blocks, Procs, and Lambdas

### Blocks

```ruby
# Blocks are chunks of code passed to methods
[1, 2, 3].each { |n| puts n }

# Multi-line block
[1, 2, 3].each do |n|
  square = n ** 2
  puts "#{n} squared is #{square}"
end

# yield - calling a block from within a method
def greet(name)
  puts "Before block"
  yield(name) if block_given?
  puts "After block"
end

greet("Alice") { |n| puts "Hello, #{n}!" }
# Before block
# Hello, Alice!
# After block

greet("Bob")  # No block given, yield is skipped
```

### Procs and Lambdas

```ruby
# Proc - stored block
square = Proc.new { |n| n ** 2 }
# Or shorthand:
square = proc { |n| n ** 2 }

puts square.call(5)    # 25
puts square.(5)        # 25 (alternative syntax)
puts square[5]         # 25 (alternative syntax)

# Using proc with methods
doubled = [1, 2, 3].map(&square)
puts doubled.inspect   # [1, 4, 9]

# Lambda - stricter proc
multiply = lambda { |a, b| a * b }
# Or shorthand:
multiply = ->(a, b) { a * b }

puts multiply.call(3, 4)  # 12
puts multiply.(3, 4)      # 12

# Key differences:
# - Lambda checks argument count; Proc doesn't
# - Lambda return exits lambda; Proc return exits enclosing method

# Symbol to proc shorthand
names = ["alice", "bob", "charlie"]
upper = names.map(&:upcase)
puts upper.inspect  # ["ALICE", "BOB", "CHARLIE"]

evens = (1..10).select(&:even?)
puts evens.inspect  # [2, 4, 6, 8, 10]
```

---

## Error Handling

### Begin-Rescue

```ruby
# Basic rescue
begin
  result = 10 / 0
rescue ZeroDivisionError => e
  puts "Error: #{e.message}"
end

# Multiple rescue blocks
begin
  # risky code
  value = Integer("abc")
rescue ZeroDivisionError => e
  puts "Division error: #{e.message}"
rescue ArgumentError => e
  puts "Argument error: #{e.message}"
rescue StandardError => e
  puts "General error: #{e.message}"
ensure
  puts "This always runs"
end

# Inline rescue
result = Integer("abc") rescue 0
puts result  # 0

# retry
attempts = 0
begin
  attempts += 1
  puts "Attempt #{attempts}"
  raise "Failed!" if attempts < 3
  puts "Success!"
rescue => e
  retry if attempts < 3
  puts "Gave up after #{attempts} attempts"
end
```

### Raising Exceptions

```ruby
# Raising exceptions
def divide(a, b)
  raise ArgumentError, "Cannot divide by zero" if b == 0
  a.to_f / b
end

begin
  puts divide(10, 0)
rescue ArgumentError => e
  puts "Caught: #{e.message}"
end

# Custom exception class
class ValidationError < StandardError
  attr_reader :field

  def initialize(field, message)
    @field = field
    super(message)
  end
end

def validate_age(age)
  raise ValidationError.new("age", "Must be between 0 and 150") unless (0..150).include?(age)
  true
end

begin
  validate_age(200)
rescue ValidationError => e
  puts "#{e.field}: #{e.message}"
end
```

---

## File Operations

### Reading and Writing Files

```ruby
filename = "example.txt"

# Writing to a file
File.write(filename, "Hello, World!\nLine 2\nLine 3\n")
puts "File written"

# Reading entire file
content = File.read(filename)
puts "Content:\n#{content}"

# Reading lines into array
lines = File.readlines(filename, chomp: true)
lines.each_with_index do |line, i|
  puts "#{i + 1}: #{line}"
end

# Reading line by line (memory efficient)
File.foreach(filename) do |line|
  puts ">> #{line.chomp}"
end

# Appending
File.open(filename, "a") do |f|
  f.puts "Appended line"
end

# Block form (auto-closes file)
File.open(filename, "r") do |f|
  f.each_line { |line| puts line.chomp }
end

# File info
puts "Exists: #{File.exist?(filename)}"
puts "Size: #{File.size(filename)} bytes"
puts "Directory: #{File.directory?(filename)}"

# Working with paths
puts File.basename("/path/to/file.txt")     # "file.txt"
puts File.dirname("/path/to/file.txt")      # "/path/to"
puts File.extname("file.txt")               # ".txt"
puts File.expand_path("~/documents")        # Full path

# Delete file
File.delete(filename)
puts "File deleted"
```

---

## Classes and Objects

### Basic Class

```ruby
class Dog
  # Constructor
  def initialize(name, breed, age)
    @name = name
    @breed = breed
    @age = age
  end

  # Getter methods (or use attr_reader)
  attr_reader :name, :breed, :age

  # Instance methods
  def bark
    puts "#{@name} says: Woof!"
  end

  def describe
    puts "#{@name} is a #{@age}-year-old #{@breed}"
  end

  def age_in_human_years
    @age * 7
  end

  # String representation
  def to_s
    "Dog(#{@name}, #{@breed}, #{@age})"
  end
end

# Creating objects
dog1 = Dog.new("Buddy", "Golden Retriever", 3)
dog2 = Dog.new("Max", "German Shepherd", 5)

dog1.bark
dog2.describe
puts dog1
puts "Human years: #{dog1.age_in_human_years}"
```

### Accessors and Encapsulation

```ruby
class BankAccount
  attr_reader :owner, :balance

  def initialize(owner, initial_balance = 0)
    @owner = owner
    @balance = [initial_balance, 0].max
  end

  def deposit(amount)
    if amount > 0
      @balance += amount
      puts "Deposited $#{'%.2f' % amount}. Balance: $#{'%.2f' % @balance}"
    end
  end

  def withdraw(amount)
    if amount > 0 && amount <= @balance
      @balance -= amount
      puts "Withdrew $#{'%.2f' % amount}. Balance: $#{'%.2f' % @balance}"
    elsif amount > @balance
      puts "Insufficient funds"
    end
  end

  def to_s
    "BankAccount(#{@owner}, $#{'%.2f' % @balance})"
  end
end

account = BankAccount.new("Alice", 1000)
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)
puts "Final balance: $#{'%.2f' % account.balance}"
```

### Inheritance and Modules

```ruby
# Base class
class Animal
  attr_reader :name, :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def eat
    puts "#{@name} is eating"
  end

  def to_s
    "#{@name} (age: #{@age})"
  end
end

# Child class
class Cat < Animal
  attr_reader :indoor

  def initialize(name, age, indoor = true)
    super(name, age)
    @indoor = indoor
  end

  def purr
    puts "#{@name} is purring"
  end

  # Override
  def eat
    puts "#{@name} is eating cat food"
  end
end

# Modules (mixins)
module Swimmable
  def swim
    puts "#{name} is swimming"
  end
end

module Flyable
  def fly
    puts "#{name} is flying"
  end
end

class Duck < Animal
  include Swimmable
  include Flyable

  def quack
    puts "#{@name} says: Quack!"
  end
end

cat = Cat.new("Whiskers", 3)
cat.eat
cat.purr

duck = Duck.new("Donald", 2)
duck.eat
duck.swim
duck.fly
duck.quack

# Check inheritance
puts Cat.ancestors.inspect
puts duck.is_a?(Animal)    # true
puts duck.is_a?(Swimmable) # true
```

---

## Practice Exercises

### Exercise 1: Temperature Converter

```ruby
def celsius_to_fahrenheit(celsius)
  (celsius * 9.0 / 5.0) + 32
end

def fahrenheit_to_celsius(fahrenheit)
  (fahrenheit - 32) * 5.0 / 9.0
end

puts "0°C = #{celsius_to_fahrenheit(0)}°F"
puts "100°C = #{celsius_to_fahrenheit(100)}°F"
puts "72°F = #{'%.1f' % fahrenheit_to_celsius(72)}°C"
```

### Exercise 2: Word Frequency Counter

```ruby
def word_frequency(text)
  words = text.downcase.scan(/\w+/)
  freq = Hash.new(0)
  words.each { |word| freq[word] += 1 }
  freq.sort_by { |_, count| -count }
end

text = "the quick brown fox jumps over the lazy dog the fox"
freq = word_frequency(text)
freq.each { |word, count| puts "#{word}: #{count}" }
```

### Exercise 3: Student Grade Manager

```ruby
class Student
  attr_reader :name

  def initialize(name)
    @name = name
    @grades = []
  end

  def add_grade(grade)
    @grades << grade if grade.between?(0, 100)
  end

  def average
    return 0 if @grades.empty?
    @grades.sum.to_f / @grades.size
  end

  def letter_grade
    case average
    when 90..100 then "A"
    when 80...90 then "B"
    when 70...80 then "C"
    when 60...70 then "D"
    else "F"
    end
  end

  def to_s
    "#{@name} - Average: #{'%.1f' % average} (#{letter_grade}), Grades: #{@grades}"
  end
end

student = Student.new("Alice")
[92, 85, 88, 95].each { |g| student.add_grade(g) }
puts student
# Alice - Average: 90.0 (A), Grades: [92, 85, 88, 95]
```

---

## Summary

These notes cover the fundamental concepts of Ruby:

1. **Variables and Types**: Dynamic typing, everything is an object, symbols, nil
2. **Operations**: Arithmetic, comparison (spaceship `<=>`), logical, method-based operators
3. **Control Flow**: if/elsif/unless, case/when with ranges and regex, pattern matching
4. **Iteration**: `times`, `each`, `map`, `select`, `reduce` — iterators over loops
5. **Methods**: Default parameters, keyword arguments, splat operators, predicate and bang methods
6. **Arrays**: Rich built-in methods, chaining, functional-style transformations
7. **Hashes**: Symbol keys, `dig` for nested access, `merge`, `transform_values`
8. **Strings**: Interpolation, heredocs, extensive built-in methods
9. **Blocks, Procs, Lambdas**: Closures, `yield`, `&:method` shorthand
10. **Error Handling**: begin/rescue/ensure, custom exceptions, retry
11. **OOP**: Classes, inheritance, modules (mixins), attr_reader/writer/accessor

### Next Steps

1. Practice the exercises and build small projects
2. Learn about Ruby gems and Bundler for dependency management
3. Explore Ruby on Rails for web development
4. Study metaprogramming (define_method, method_missing, open classes)
5. Learn about testing with RSpec or Minitest

### Additional Resources

- **Ruby Documentation**: https://ruby-doc.org/
- **Ruby Style Guide**: https://rubystyle.guide/
- **Ruby on Rails Guides**: https://guides.rubyonrails.org/
- **Try Ruby**: https://try.ruby-lang.org/
- **Practice Problems**: https://exercism.org/tracks/ruby
