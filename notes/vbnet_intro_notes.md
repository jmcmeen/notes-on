# Elementary VB.NET Programming Concepts

## Table of Contents

1. [Getting Started with VB.NET](#getting-started-with-vbnet)
2. [Variables and Data Types](#variables-and-data-types)
3. [Basic Operations](#basic-operations)
4. [Input and Output](#input-and-output)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Methods and Functions](#methods-and-functions)
8. [Arrays and Collections](#arrays-and-collections)
9. [String Manipulation](#string-manipulation)
10. [Error Handling](#error-handling)
11. [File Operations](#file-operations)
12. [Classes and Objects](#classes-and-objects)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## Getting Started with VB.NET

### What is VB.NET?

VB.NET (Visual Basic .NET) is an object-oriented programming language on the .NET platform. Key features:
- **Readable syntax**: Designed to be approachable with English-like keywords
- **Strongly typed**: Variables must be declared with specific types (with Option Strict)
- **Object-oriented**: Full support for classes, inheritance, and interfaces
- **Case-insensitive**: `MyVariable` and `myvariable` are the same
- **Event-driven**: Natural fit for Windows desktop applications (WinForms, WPF)
- **Cross-platform**: Runs on Windows, Mac, Linux with .NET

### Your First VB.NET Program

```vb
Module Program
    Sub Main()
        ' This is a comment
        Console.WriteLine("Hello, World!")
        Console.ReadKey() ' Wait for key press
    End Sub
End Module
```

**Output:**
```
Hello, World!
```

### Program Structure Explained

- **Module Program** - A module containing code (similar to a static class)
- **Sub Main()** - Entry point of the program
- **Console.WriteLine()** - Prints text with a newline
- **Console.Write()** - Prints text without a newline
- **'** - Single-line comment
- **REM** - Alternative single-line comment keyword
- Statements do not need semicolons; each line is a statement

### Development Environment

- **Visual Studio**: Full-featured IDE (recommended)
- **Visual Studio Code**: Lightweight editor with VB extensions
- **JetBrains Rider**: Professional IDE
- **.NET SDK**: Required to compile and run VB.NET programs

### Compiling and Running

```bash
dotnet new console --language VB -o MyApp   # Create new project
cd MyApp
dotnet run                                    # Build and run
dotnet build                                  # Build only
```

---

## Variables and Data Types

### Variable Declaration

```vb
Module Program
    Sub Main()
        ' Declaring variables with Dim
        Dim name As String = "Alice"
        Dim age As Integer = 25
        Dim height As Double = 5.6
        Dim isStudent As Boolean = True

        Console.WriteLine($"Name: {name}")
        Console.WriteLine($"Age: {age}")
        Console.WriteLine($"Height: {height}")
        Console.WriteLine($"Is Student: {isStudent}")

        ' Type inference with Dim (Option Infer On)
        Dim city = "New York"        ' Inferred as String
        Dim count = 42               ' Inferred as Integer
        Dim price = 19.99            ' Inferred as Double
    End Sub
End Module
```

### Basic Data Types

```vb
' Integer Types
Dim byteVal As Byte = 255              ' 0 to 255
Dim shortVal As Short = 32000          ' -32,768 to 32,767
Dim intVal As Integer = 2000000        ' -2.1 billion to 2.1 billion
Dim longVal As Long = 9000000000L      ' Very large integers

' Floating Point Types
Dim singleVal As Single = 3.14F        ' 7 digits precision
Dim doubleVal As Double = 19.99        ' 15-17 digits precision
Dim decimalVal As Decimal = 1000.50D   ' 28-29 digits (financial)

' Character and String
Dim grade As Char = "A"c               ' Single character
Dim firstName As String = "John"

' Boolean
Dim isValid As Boolean = True
Dim isEmpty As Boolean = False

' Date
Dim today As Date = Date.Now
Dim birthday As Date = #12/25/2000#    ' Date literal

Console.WriteLine($"Date: {today:yyyy-MM-dd}")
Console.WriteLine($"Type of intVal: {intVal.GetType()}")
```

### Type Conversion

```vb
' Implicit conversion (widening)
Dim intNum As Integer = 42
Dim dblNum As Double = intNum   ' Integer to Double (safe)

' Explicit conversion (narrowing)
Dim d As Double = 3.99
Dim i As Integer = CInt(d)      ' 4 (rounds)
Dim i2 As Integer = CType(d, Integer)

' Conversion functions
Dim s As String = "42"
Dim num As Integer = CInt(s)        ' Convert to Integer
Dim lng As Long = CLng("1000000")    ' Convert to Long
Dim dbl As Double = CDbl("3.14")    ' Convert to Double
Dim str As String = CStr(42)        ' Convert to String
Dim bln As Boolean = CBool(1)       ' Convert to Boolean

' Parse and TryParse
Dim parsed As Integer = Integer.Parse("42")

Dim result As Integer
If Integer.TryParse("42abc", result) Then
    Console.WriteLine($"Parsed: {result}")
Else
    Console.WriteLine("Could not parse")
End If

' ToString with formatting
Console.WriteLine(3.14159.ToString("F2"))    ' "3.14"
Console.WriteLine(1234.56.ToString("C"))      ' "$1,234.56"
Console.WriteLine(0.85.ToString("P"))         ' "85.00%"
```

### Constants and Enumerations

```vb
' Constants
Const PI As Double = 3.14159
Const MAX_SIZE As Integer = 100
Const COMPANY As String = "TechCorp"

' Enumerations
Enum DayOfWeek
    Monday = 1
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
    Sunday
End Enum

Dim today As DayOfWeek = DayOfWeek.Wednesday
Console.WriteLine($"Today is {today}")         ' "Wednesday"
Console.WriteLine($"Day number: {CInt(today)}") ' 3
```

---

## Basic Operations

### Arithmetic Operators

```vb
Dim a As Integer = 10
Dim b As Integer = 3

Console.WriteLine($"10 + 3 = {a + b}")        ' 13
Console.WriteLine($"10 - 3 = {a - b}")        ' 7
Console.WriteLine($"10 * 3 = {a * b}")        ' 30
Console.WriteLine($"10 / 3 = {a / b}")        ' 3.333... (floating point division)
Console.WriteLine($"10 \ 3 = {a \ b}")        ' 3 (integer division)
Console.WriteLine($"10 Mod 3 = {a Mod b}")    ' 1 (remainder)
Console.WriteLine($"10 ^ 3 = {a ^ b}")        ' 1000 (exponentiation)

' Compound assignment
Dim x As Integer = 5
x += 3    ' 8
x -= 2    ' 6
x *= 2    ' 12
x \= 4   ' 3 (integer division assignment)

Console.WriteLine($"Final x: {x}")

' Math class methods
Console.WriteLine($"Abs(-5): {Math.Abs(-5)}")
Console.WriteLine($"Max(3,7): {Math.Max(3, 7)}")
Console.WriteLine($"Min(3,7): {Math.Min(3, 7)}")
Console.WriteLine($"Round(3.7): {Math.Round(3.7)}")
Console.WriteLine($"Floor(3.7): {Math.Floor(3.7)}")
Console.WriteLine($"Ceiling(3.2): {Math.Ceiling(3.2)}")
Console.WriteLine($"Sqrt(16): {Math.Sqrt(16)}")
```

### Comparison Operators

```vb
Dim x As Integer = 5
Dim y As Integer = 10

Console.WriteLine($"5 = 10: {x = y}")     ' False (= is comparison in context)
Console.WriteLine($"5 <> 10: {x <> y}")   ' True (not equal)
Console.WriteLine($"5 < 10: {x < y}")     ' True
Console.WriteLine($"5 > 10: {x > y}")     ' False
Console.WriteLine($"5 <= 10: {x <= y}")   ' True
Console.WriteLine($"5 >= 10: {x >= y}")   ' False
```

### Logical Operators

```vb
Dim a As Boolean = True
Dim b As Boolean = False

Console.WriteLine($"True And False: {a And b}")       ' False
Console.WriteLine($"True Or False: {a Or b}")         ' True
Console.WriteLine($"Not True: {Not a}")               ' False
Console.WriteLine($"True Xor False: {a Xor b}")      ' True

' Short-circuit operators (preferred)
Console.WriteLine($"True AndAlso False: {a AndAlso b}")  ' False
Console.WriteLine($"True OrElse False: {a OrElse b}")    ' True

' Practical example
Dim age As Integer = 20
Dim hasLicense As Boolean = True
Dim canDrive As Boolean = age >= 18 AndAlso hasLicense
Console.WriteLine($"Can drive: {canDrive}")
```

### String Operators

```vb
' Concatenation
Dim first As String = "Hello"
Dim second As String = "World"
Dim combined As String = first & ", " & second & "!"
Console.WriteLine(combined)  ' "Hello, World!"

' String interpolation (preferred)
Dim name As String = "Alice"
Dim age As Integer = 25
Console.WriteLine($"Name: {name}, Age: {age}")

' Like operator (pattern matching)
Console.WriteLine("Hello" Like "H*")        ' True
Console.WriteLine("Hello" Like "H???o")     ' True
Console.WriteLine("ABC123" Like "???###")   ' True
```

---

## Input and Output

### Console Output

```vb
Dim name As String = "Alice"
Dim age As Integer = 25
Dim gpa As Double = 3.85

' Different output methods
Console.WriteLine("Hello, World!")                   ' With newline
Console.Write("No newline ")                         ' Without newline
Console.WriteLine()                                  ' Just newline

' String interpolation
Console.WriteLine($"Name: {name}, Age: {age}")
Console.WriteLine($"GPA: {gpa:F2}")                 ' 2 decimal places
Console.WriteLine($"Date: {Date.Now:yyyy-MM-dd}")

' Composite formatting
Console.WriteLine("Name: {0}, Age: {1}", name, age)
Console.WriteLine("GPA: {0:F2}", gpa)

' Format specifiers
Dim money As Double = 1234.56
Console.WriteLine($"Currency: {money:C}")            ' $1,234.56
Console.WriteLine($"Percentage: {0.85:P}")           ' 85.00%
Console.WriteLine($"Padded: {age,10}")               ' Right-aligned in 10 chars
Console.WriteLine($"Padded: {age,-10}|")             ' Left-aligned in 10 chars
```

### Console Input

```vb
' Reading string input
Console.Write("What's your name? ")
Dim name As String = Console.ReadLine()
Console.WriteLine($"Hello, {name}!")

' Reading numeric input
Console.Write("How old are you? ")
Dim ageInput As String = Console.ReadLine()
Dim age As Integer

If Integer.TryParse(ageInput, age) Then
    Console.WriteLine($"You are {age} years old")
Else
    Console.WriteLine("Invalid age entered")
End If

' Reading a single key
Console.Write("Press any key...")
Dim keyInfo As ConsoleKeyInfo = Console.ReadKey()
Console.WriteLine($"{vbCrLf}You pressed: {keyInfo.Key}")
```

---

## Conditional Statements

### If...Then...Else

```vb
' Basic If
Dim age As Integer = 18

If age >= 18 Then
    Console.WriteLine("You are an adult")
    Console.WriteLine("You can vote")
End If

' If-Else
Dim temperature As Integer = 25

If temperature > 30 Then
    Console.WriteLine("It's hot outside")
Else
    Console.WriteLine("It's not too hot")
End If

' If-ElseIf-Else
Dim score As Integer = 85
Dim grade As String

If score >= 90 Then
    grade = "A"
ElseIf score >= 80 Then
    grade = "B"
ElseIf score >= 70 Then
    grade = "C"
ElseIf score >= 60 Then
    grade = "D"
Else
    grade = "F"
End If

Console.WriteLine($"Your grade is: {grade}")

' Single-line If
If age >= 18 Then Console.WriteLine("Adult")
```

### Select Case

```vb
' Select Case (like switch)
Dim dayNumber As Integer = 3
Dim dayName As String

Select Case dayNumber
    Case 1
        dayName = "Monday"
    Case 2
        dayName = "Tuesday"
    Case 3
        dayName = "Wednesday"
    Case 4
        dayName = "Thursday"
    Case 5
        dayName = "Friday"
    Case 6, 7
        dayName = "Weekend"
    Case Else
        dayName = "Invalid day"
End Select

Console.WriteLine($"Day {dayNumber} is {dayName}")

' Select Case with ranges
Dim age As Integer = 25

Select Case age
    Case 0 To 12
        Console.WriteLine("Child")
    Case 13 To 17
        Console.WriteLine("Teenager")
    Case 18 To 64
        Console.WriteLine("Adult")
    Case Is >= 65
        Console.WriteLine("Senior")
    Case Else
        Console.WriteLine("Invalid age")
End Select

' Select Case with strings
Dim command As String = "start"

Select Case command.ToLower()
    Case "start"
        Console.WriteLine("Starting...")
    Case "stop"
        Console.WriteLine("Stopping...")
    Case "pause", "suspend"
        Console.WriteLine("Pausing...")
    Case Else
        Console.WriteLine("Unknown command")
End Select
```

### Ternary-Style Expressions

```vb
' VB.NET uses If() function instead of ternary operator
Dim age As Integer = 20
Dim status As String = If(age >= 18, "Adult", "Minor")
Console.WriteLine($"Status: {status}")

' Null coalescing
Dim input As String = Nothing
Dim value As String = If(input, "default")
Console.WriteLine($"Value: {value}")  ' "default"

' IIf function (evaluates both sides - use If() instead)
' Dim result = IIf(x > 0, "positive", "non-positive")  ' Legacy
```

---

## Loops

### For...Next Loop

```vb
' Basic For loop
Console.WriteLine("Counting to 5:")
For i As Integer = 1 To 5
    Console.WriteLine($"Count: {i}")
Next

' With Step
Console.WriteLine(vbCrLf & "Even numbers from 2 to 10:")
For i As Integer = 2 To 10 Step 2
    Console.WriteLine(i)
Next

' Counting backwards
Console.WriteLine(vbCrLf & "Countdown:")
For i As Integer = 5 To 1 Step -1
    Console.WriteLine(i)
Next
Console.WriteLine("Blast off!")
```

### For Each...Next Loop

```vb
' Iterating over arrays
Dim fruits() As String = {"apple", "banana", "cherry"}

Console.WriteLine("Fruits:")
For Each fruit As String In fruits
    Console.WriteLine($"- {fruit}")
Next

' Iterating over collections
Dim numbers As New List(Of Integer) From {1, 2, 3, 4, 5}
Dim sum As Integer = 0

For Each num As Integer In numbers
    sum += num
Next

Console.WriteLine($"Sum: {sum}")

' Iterating over string characters
Dim word As String = "Hello"
For Each ch As Char In word
    Console.WriteLine(ch)
Next
```

### While and Do...Loop

```vb
' While loop
Dim count As Integer = 0
While count < 3
    Console.WriteLine($"Count: {count}")
    count += 1
End While

' Do While (condition at top)
Dim x As Integer = 0
Do While x < 3
    Console.WriteLine($"x = {x}")
    x += 1
Loop

' Do Until (opposite condition at top)
Dim y As Integer = 0
Do Until y >= 3
    Console.WriteLine($"y = {y}")
    y += 1
Loop

' Do...Loop While (condition at bottom, runs at least once)
Dim input As String
Do
    Console.Write("Enter 'quit' to exit: ")
    input = Console.ReadLine()
    Console.WriteLine($"You entered: {input}")
Loop While input <> "quit"

' Do...Loop Until
Dim guess As Integer
Do
    Console.Write("Guess (1-10): ")
    guess = CInt(Console.ReadLine())
Loop Until guess = 7
Console.WriteLine("Correct!")
```

### Loop Control

```vb
' Exit For - break out of loop
Console.WriteLine("Exit For:")
For i As Integer = 0 To 9
    If i = 5 Then Exit For
    Console.Write($"{i} ")
Next
Console.WriteLine()

' Continue For - skip to next iteration
Console.WriteLine("Continue For:")
For i As Integer = 0 To 9
    If i Mod 3 = 0 Then Continue For
    Console.Write($"{i} ")
Next
Console.WriteLine()

' Exit While, Exit Do also available
Dim n As Integer = 0
While True
    If n >= 5 Then Exit While
    n += 1
End While
```

---

## Methods and Functions

### Sub Procedures (No Return Value)

```vb
Module Program
    ' Sub - no return value
    Sub SayHello()
        Console.WriteLine("Hello from a sub!")
    End Sub

    ' Sub with parameters
    Sub GreetPerson(name As String)
        Console.WriteLine($"Hello, {name}!")
    End Sub

    ' Sub with ByRef parameter (modifies original)
    Sub DoubleValue(ByRef value As Integer)
        value *= 2
    End Sub

    Sub Main()
        SayHello()
        GreetPerson("Alice")

        Dim num As Integer = 5
        DoubleValue(num)
        Console.WriteLine($"Doubled: {num}")  ' 10
    End Sub
End Module
```

### Functions (With Return Value)

```vb
Module Program
    ' Function with return value
    Function AddNumbers(a As Integer, b As Integer) As Integer
        Return a + b
    End Function

    ' Function with default parameter
    Function Greet(name As String, Optional greeting As String = "Hello") As String
        Return $"{greeting}, {name}!"
    End Function

    ' Function with multiple return via tuple
    Function GetMinMax(numbers() As Integer) As (Min As Integer, Max As Integer)
        Return (numbers.Min(), numbers.Max())
    End Function

    Sub Main()
        Console.WriteLine($"5 + 3 = {AddNumbers(5, 3)}")

        Console.WriteLine(Greet("Alice"))
        Console.WriteLine(Greet("Bob", "Hi"))

        Dim nums() As Integer = {3, 7, 1, 9, 4}
        Dim result = GetMinMax(nums)
        Console.WriteLine($"Min: {result.Min}, Max: {result.Max}")
    End Sub
End Module
```

### Overloading and ParamArray

```vb
Module Program
    ' Method overloading
    Function Add(a As Integer, b As Integer) As Integer
        Return a + b
    End Function

    Function Add(a As Double, b As Double) As Double
        Return a + b
    End Function

    Function Add(a As Integer, b As Integer, c As Integer) As Integer
        Return a + b + c
    End Function

    ' ParamArray - variable number of arguments
    Function SumAll(ParamArray numbers() As Integer) As Integer
        Return numbers.Sum()
    End Function

    Sub Main()
        Console.WriteLine(Add(5, 3))          ' Integer version
        Console.WriteLine(Add(5.5, 3.2))      ' Double version
        Console.WriteLine(Add(1, 2, 3))       ' Three-parameter version

        Console.WriteLine(SumAll(1, 2, 3))         ' 6
        Console.WriteLine(SumAll(1, 2, 3, 4, 5))   ' 15
    End Sub
End Module
```

---

## Arrays and Collections

### Arrays

```vb
' Declaring arrays
Dim numbers(4) As Integer              ' Array of 5 elements (0 to 4)
Dim fruits() As String = {"apple", "banana", "cherry"}
Dim matrix(,) As Integer = {{1, 2, 3}, {4, 5, 6}}

' Accessing elements
numbers(0) = 10
numbers(1) = 20
numbers(2) = 30

Console.WriteLine($"First fruit: {fruits(0)}")
Console.WriteLine($"Array length: {fruits.Length}")

' Looping through arrays
Console.WriteLine("Numbers:")
For i As Integer = 0 To numbers.Length - 1
    Console.WriteLine($"numbers({i}) = {numbers(i)}")
Next

Console.WriteLine("Fruits:")
For Each fruit As String In fruits
    Console.WriteLine($"- {fruit}")
Next

' Array methods
Dim arr() As Integer = {5, 2, 8, 1, 9}
Array.Sort(arr)
Console.WriteLine($"Sorted: {String.Join(", ", arr)}")

Array.Reverse(arr)
Console.WriteLine($"Reversed: {String.Join(", ", arr)}")

Dim index As Integer = Array.IndexOf(arr, 5)
Console.WriteLine($"Index of 5: {index}")

' Resizing
ReDim Preserve numbers(9)   ' Resize to 10 elements, keep existing
```

### List(Of T)

```vb
Imports System.Collections.Generic

' Creating lists
Dim names As New List(Of String)
Dim numbers As New List(Of Integer) From {1, 2, 3, 4, 5}

' Adding elements
names.Add("Alice")
names.Add("Bob")
names.Add("Charlie")
names.Insert(1, "David")

' Accessing
Console.WriteLine($"First: {names(0)}")
Console.WriteLine($"Count: {names.Count}")

' Removing
names.Remove("Bob")
names.RemoveAt(0)

' Searching
Console.WriteLine($"Contains Charlie: {names.Contains("Charlie")}")
Console.WriteLine($"Index of Charlie: {names.IndexOf("Charlie")}")

' Iterating
For Each name As String In names
    Console.WriteLine($"- {name}")
Next

' LINQ operations
Dim sorted = numbers.OrderBy(Function(n) n).ToList()
Dim evens = numbers.Where(Function(n) n Mod 2 = 0).ToList()
Dim doubled = numbers.Select(Function(n) n * 2).ToList()
Dim sum As Integer = numbers.Sum()

Console.WriteLine($"Sum: {sum}")
Console.WriteLine($"Evens: {String.Join(", ", evens)}")
```

### Dictionary(Of TKey, TValue)

```vb
Imports System.Collections.Generic

' Creating dictionaries
Dim ages As New Dictionary(Of String, Integer)
Dim capitals As New Dictionary(Of String, String) From {
    {"USA", "Washington D.C."},
    {"France", "Paris"},
    {"Japan", "Tokyo"}
}

' Adding
ages("Alice") = 25
ages("Bob") = 30
ages.Add("Charlie", 35)

' Accessing
Console.WriteLine($"Alice's age: {ages("Alice")}")
Console.WriteLine($"Capital of France: {capitals("France")}")

' Safe access
Dim value As Integer
If ages.TryGetValue("David", value) Then
    Console.WriteLine($"David's age: {value}")
Else
    Console.WriteLine("David not found")
End If

' Checking
Console.WriteLine($"Has Bob: {ages.ContainsKey("Bob")}")
Console.WriteLine($"Has age 25: {ages.ContainsValue(25)}")

' Modifying and removing
ages("Alice") = 26
ages.Remove("Charlie")

' Iterating
For Each kvp As KeyValuePair(Of String, Integer) In ages
    Console.WriteLine($"{kvp.Key}: {kvp.Value}")
Next

Console.WriteLine($"Keys: {String.Join(", ", ages.Keys)}")
Console.WriteLine($"Values: {String.Join(", ", ages.Values)}")
```

---

## String Manipulation

### String Basics

```vb
Dim text As String = "Hello, World!"

' Properties and methods
Console.WriteLine($"Length: {text.Length}")
Console.WriteLine($"Upper: {text.ToUpper()}")
Console.WriteLine($"Lower: {text.ToLower()}")

' Checking
Console.WriteLine($"Starts with Hello: {text.StartsWith("Hello")}")
Console.WriteLine($"Ends with !: {text.EndsWith("!")}")
Console.WriteLine($"Contains World: {text.Contains("World")}")
Console.WriteLine($"Is null or empty: {String.IsNullOrEmpty(text)}")
Console.WriteLine($"Is null or whitespace: {String.IsNullOrWhiteSpace(text)}")

' Accessing characters
Console.WriteLine($"First char: {text(0)}")
Console.WriteLine($"Last char: {text(text.Length - 1)}")

' Finding
Console.WriteLine($"IndexOf World: {text.IndexOf("World")}")
Console.WriteLine($"LastIndexOf l: {text.LastIndexOf("l"c)}")
```

### String Manipulation

```vb
Dim text As String = "Hello, World!"

' Substring
Console.WriteLine(text.Substring(0, 5))    ' "Hello"
Console.WriteLine(text.Substring(7))        ' "World!"

' Replacing
Console.WriteLine(text.Replace("World", "VB.NET"))

' Trimming
Dim padded As String = "  Hello, World!  "
Console.WriteLine($"Trim: '{padded.Trim()}'")
Console.WriteLine($"TrimStart: '{padded.TrimStart()}'")
Console.WriteLine($"TrimEnd: '{padded.TrimEnd()}'")

' Splitting and joining
Dim csv As String = "apple,banana,cherry,date"
Dim parts() As String = csv.Split(","c)
For Each part As String In parts
    Console.WriteLine($"- {part}")
Next

Dim joined As String = String.Join(" | ", parts)
Console.WriteLine(joined)

' Padding
Console.WriteLine("5".PadLeft(5, "0"c))      ' "00005"
Console.WriteLine("Hi".PadRight(10, "."c))    ' "Hi........"

' StringBuilder for efficient concatenation
Dim sb As New System.Text.StringBuilder()
For i As Integer = 0 To 4
    sb.Append($"Item {i}, ")
Next
Console.WriteLine(sb.ToString())

' String comparison
Console.WriteLine(String.Equals("hello", "Hello", StringComparison.OrdinalIgnoreCase))  ' True
Console.WriteLine(String.Compare("abc", "def"))  ' Negative
```

---

## Error Handling

### Try...Catch...Finally

```vb
' Basic Try-Catch
Try
    Dim result As Integer = 10 \ 0
    Console.WriteLine(result)
Catch ex As DivideByZeroException
    Console.WriteLine($"Error: {ex.Message}")
End Try

' Multiple Catch blocks
Try
    Dim numbers() As Integer = {1, 2, 3}
    Console.WriteLine(numbers(10))
Catch ex As IndexOutOfRangeException
    Console.WriteLine($"Index error: {ex.Message}")
Catch ex As Exception
    Console.WriteLine($"General error: {ex.Message}")
Finally
    Console.WriteLine("This always runs")
End Try

' TryParse pattern (avoid exceptions for expected failures)
Dim input As String = "not a number"
Dim number As Integer

If Integer.TryParse(input, number) Then
    Console.WriteLine($"Parsed: {number}")
Else
    Console.WriteLine("Could not parse input")
End If
```

### Throwing Exceptions

```vb
Function Divide(a As Double, b As Double) As Double
    If b = 0 Then
        Throw New ArgumentException("Cannot divide by zero")
    End If
    Return a / b
End Function

' Custom exception
Class ValidationException
    Inherits Exception

    Public ReadOnly Property Field As String

    Sub New(field As String, message As String)
        MyBase.New(message)
        Me.Field = field
    End Sub
End Class

Sub ValidateAge(age As Integer)
    If age < 0 OrElse age > 150 Then
        Throw New ValidationException("age", "Age must be between 0 and 150")
    End If
End Sub

' Usage
Try
    ValidateAge(200)
Catch ex As ValidationException
    Console.WriteLine($"{ex.Field}: {ex.Message}")
End Try
```

---

## File Operations

### Reading and Writing Files

```vb
Imports System.IO

Dim filename As String = "example.txt"

' Writing to a file
File.WriteAllText(filename, "Hello, World!" & vbCrLf & "Line 2" & vbCrLf & "Line 3")
Console.WriteLine("File written")

' Reading entire file
Dim content As String = File.ReadAllText(filename)
Console.WriteLine($"Content:{vbCrLf}{content}")

' Reading all lines
Dim lines() As String = File.ReadAllLines(filename)
For i As Integer = 0 To lines.Length - 1
    Console.WriteLine($"{i + 1}: {lines(i)}")
Next

' Appending
File.AppendAllText(filename, "Appended line" & vbCrLf)

' Writing lines
Dim data() As String = {"Line A", "Line B", "Line C"}
File.WriteAllLines("output.txt", data)

' StreamReader for large files
Using reader As New StreamReader(filename)
    Dim line As String
    Do
        line = reader.ReadLine()
        If line IsNot Nothing Then
            Console.WriteLine($">> {line}")
        End If
    Loop Until line Is Nothing
End Using

' File info
Console.WriteLine($"Exists: {File.Exists(filename)}")
Dim info As New FileInfo(filename)
Console.WriteLine($"Size: {info.Length} bytes")
Console.WriteLine($"Created: {info.CreationTime}")

' Delete
File.Delete(filename)
File.Delete("output.txt")
```

---

## Classes and Objects

### Basic Class

```vb
Class Dog
    ' Properties
    Public Property Name As String
    Public Property Breed As String
    Public Property Age As Integer

    ' Constructor
    Sub New(name As String, breed As String, age As Integer)
        Me.Name = name
        Me.Breed = breed
        Me.Age = age
    End Sub

    ' Default constructor
    Sub New()
        Name = "Unknown"
        Breed = "Mixed"
        Age = 0
    End Sub

    ' Methods
    Sub Bark()
        Console.WriteLine($"{Name} says: Woof!")
    End Sub

    Sub Describe()
        Console.WriteLine($"{Name} is a {Age}-year-old {Breed}")
    End Sub

    Function GetAgeInHumanYears() As Integer
        Return Age * 7
    End Function

    ' Override ToString
    Public Overrides Function ToString() As String
        Return $"Dog({Name}, {Breed}, {Age})"
    End Function
End Class

' Usage
Dim dog1 As New Dog("Buddy", "Golden Retriever", 3)
Dim dog2 As New Dog("Max", "German Shepherd", 5)
Dim dog3 As New Dog()

dog1.Bark()
dog2.Describe()
Console.WriteLine(dog1)
Console.WriteLine($"Human years: {dog1.GetAgeInHumanYears()}")
```

### Inheritance and Interfaces

```vb
' Base class
MustInherit Class Animal
    Public Property Name As String
    Public Property Age As Integer

    Sub New(name As String, age As Integer)
        Me.Name = name
        Me.Age = age
    End Sub

    Overridable Sub Eat()
        Console.WriteLine($"{Name} is eating")
    End Sub

    Public Overrides Function ToString() As String
        Return $"{Name} (age: {Age})"
    End Function
End Class

' Derived class
Class Cat
    Inherits Animal

    Public Property IsIndoor As Boolean

    Sub New(name As String, age As Integer, Optional isIndoor As Boolean = True)
        MyBase.New(name, age)
        Me.IsIndoor = isIndoor
    End Sub

    Sub Purr()
        Console.WriteLine($"{Name} is purring")
    End Sub

    ' Override parent method
    Public Overrides Sub Eat()
        Console.WriteLine($"{Name} is eating cat food")
    End Sub
End Class

' Interface
Interface IDrawable
    Sub Draw()
    Function GetArea() As Double
End Interface

Class Circle
    Implements IDrawable

    Public Property Radius As Double

    Sub New(radius As Double)
        Me.Radius = radius
    End Sub

    Public Sub Draw() Implements IDrawable.Draw
        Console.WriteLine($"Drawing circle with radius {Radius}")
    End Sub

    Public Function GetArea() As Double Implements IDrawable.GetArea
        Return Math.PI * Radius ^ 2
    End Function
End Class

' Usage
Dim cat As New Cat("Whiskers", 3)
cat.Eat()
cat.Purr()

Dim circle As New Circle(5)
circle.Draw()
Console.WriteLine($"Area: {circle.GetArea():F2}")
```

---

## Practice Exercises

### Exercise 1: Temperature Converter

```vb
Function CelsiusToFahrenheit(celsius As Double) As Double
    Return (celsius * 9.0 / 5.0) + 32
End Function

Function FahrenheitToCelsius(fahrenheit As Double) As Double
    Return (fahrenheit - 32) * 5.0 / 9.0
End Function

' Test
Console.WriteLine($"0°C = {CelsiusToFahrenheit(0)}°F")
Console.WriteLine($"100°C = {CelsiusToFahrenheit(100)}°F")
Console.WriteLine($"72°F = {FahrenheitToCelsius(72):F1}°C")
```

### Exercise 2: Simple Calculator

```vb
Console.Write("Enter first number: ")
Dim num1 As Double = CDbl(Console.ReadLine())

Console.Write("Enter operator (+, -, *, /): ")
Dim op As String = Console.ReadLine()

Console.Write("Enter second number: ")
Dim num2 As Double = CDbl(Console.ReadLine())

Dim result As Double

Select Case op
    Case "+"
        result = num1 + num2
    Case "-"
        result = num1 - num2
    Case "*"
        result = num1 * num2
    Case "/"
        If num2 <> 0 Then
            result = num1 / num2
        Else
            Console.WriteLine("Error: Division by zero")
            Return
        End If
    Case Else
        Console.WriteLine("Invalid operator")
        Return
End Select

Console.WriteLine($"{num1} {op} {num2} = {result:F2}")
```

### Exercise 3: Student Grade Manager

```vb
Class Student
    Private _grades As New List(Of Double)

    Public ReadOnly Property Name As String

    Sub New(name As String)
        Me.Name = name
    End Sub

    Sub AddGrade(grade As Double)
        If grade >= 0 AndAlso grade <= 100 Then
            _grades.Add(grade)
        End If
    End Sub

    Function GetAverage() As Double
        If _grades.Count = 0 Then Return 0
        Return _grades.Average()
    End Function

    Function GetLetterGrade() As String
        Dim avg = GetAverage()
        Select Case avg
            Case >= 90 : Return "A"
            Case >= 80 : Return "B"
            Case >= 70 : Return "C"
            Case >= 60 : Return "D"
            Case Else : Return "F"
        End Select
    End Function

    Public Overrides Function ToString() As String
        Return $"{Name} - Average: {GetAverage():F1} ({GetLetterGrade()}), Grades: [{String.Join(", ", _grades)}]"
    End Function
End Class

' Usage
Dim student As New Student("Alice")
student.AddGrade(92)
student.AddGrade(85)
student.AddGrade(88)
student.AddGrade(95)
Console.WriteLine(student)
' Alice - Average: 90.0 (A), Grades: [92, 85, 88, 95]
```

---

## Summary

These notes cover the fundamental concepts of VB.NET:

1. **Variables and Types**: `Dim`, strong typing, type inference, `Enum`, `Const`
2. **Operations**: Arithmetic (`\` for integer division, `Mod`), comparison (`<>`), logical (`AndAlso`, `OrElse`)
3. **Strings**: `&` concatenation, `$""` interpolation, `Like` pattern matching
4. **Control Flow**: `If...ElseIf...Else`, `Select Case` with ranges, `If()` function
5. **Loops**: `For...Next`, `For Each`, `While`, `Do...Loop While/Until`
6. **Methods**: `Sub` (no return) and `Function` (with return), `Optional`, `ParamArray`, `ByRef`
7. **Arrays and Collections**: Arrays, `List(Of T)`, `Dictionary(Of TKey, TValue)`, LINQ
8. **Error Handling**: `Try...Catch...Finally`, `TryParse` pattern, custom exceptions
9. **File Operations**: `File.ReadAllText/WriteAllText`, `StreamReader/StreamWriter`
10. **OOP**: Classes, properties, inheritance (`Inherits`), interfaces (`Implements`), `MustInherit`

### Next Steps

1. Practice the exercises and build Windows Forms applications
2. Learn about LINQ for data querying
3. Explore WPF for modern desktop UIs
4. Study ASP.NET for web development with VB.NET
5. Learn about async/await for asynchronous programming

### Additional Resources

- **VB.NET Documentation**: https://learn.microsoft.com/en-us/dotnet/visual-basic/
- **.NET API Browser**: https://learn.microsoft.com/en-us/dotnet/api/
- **VB.NET Language Reference**: https://learn.microsoft.com/en-us/dotnet/visual-basic/language-reference/
- **Practice Problems**: https://exercism.org/tracks/vb-net
