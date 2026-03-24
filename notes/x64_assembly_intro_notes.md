# Elementary x64 Assembly Programming Concepts

## Table of Contents

1. [Getting Started with x64 Assembly](#getting-started-with-x64-assembly)
2. [Registers](#registers)
3. [Data Types and Memory](#data-types-and-memory)
4. [Basic Instructions](#basic-instructions)
5. [Arithmetic and Logic](#arithmetic-and-logic)
6. [Control Flow](#control-flow)
7. [The Stack](#the-stack)
8. [Functions and Calling Conventions](#functions-and-calling-conventions)
9. [Memory Addressing Modes](#memory-addressing-modes)
10. [String and Array Operations](#string-and-array-operations)
11. [System Calls (Linux)](#system-calls-linux)
12. [Floating Point (SSE/AVX)](#floating-point-sseavx)
13. [Debugging and Tools](#debugging-and-tools)
14. [Practice Exercises](#practice-exercises)
15. [Summary](#summary)

---

## Getting Started with x64 Assembly

### What is x64 Assembly?

x64 assembly (also called x86-64 or AMD64) is a low-level programming language that maps directly to the instruction set of 64-bit x86 processors. Key characteristics:
- **Lowest level above machine code**: Each instruction maps to a CPU operation
- **Architecture specific**: Written for x86-64 processors (Intel and AMD)
- **Direct hardware control**: Direct access to registers, memory, and I/O
- **Maximum performance**: No abstraction overhead
- **Two main syntaxes**: Intel syntax (used here) and AT&T syntax
- **Uses**: OS kernels, drivers, performance-critical code, reverse engineering, CTFs

### Your First x64 Assembly Program (Linux, NASM)

```asm
; hello.asm - Hello World in x64 assembly (NASM, Linux)
section .data
    msg db "Hello, World!", 10    ; string with newline (10 = '\n')
    msg_len equ $ - msg           ; calculate string length

section .text
    global _start

_start:
    ; sys_write(stdout, msg, msg_len)
    mov rax, 1          ; syscall number for sys_write
    mov rdi, 1          ; file descriptor 1 = stdout
    mov rsi, msg        ; pointer to message
    mov rdx, msg_len    ; message length
    syscall             ; invoke kernel

    ; sys_exit(0)
    mov rax, 60         ; syscall number for sys_exit
    xor rdi, rdi        ; exit code 0
    syscall             ; invoke kernel
```

**Output:**
```
Hello, World!
```

### Assembling and Running

```bash
# Assemble with NASM
nasm -f elf64 hello.asm -o hello.o

# Link with ld
ld hello.o -o hello

# Run
./hello
```

### Program Structure Explained

- **section .data** - Initialized data (global variables, string constants)
- **section .bss** - Uninitialized data (reserved memory)
- **section .text** - Code (executable instructions)
- **global _start** - Export the entry point for the linker
- **_start:** - Label marking the program entry point
- **;** - Comment (everything after semicolon on a line)
- **mov** - Move (copy) data between registers/memory
- **syscall** - Invoke a Linux kernel system call

### Development Environment

- **NASM**: Netwide Assembler (Intel syntax, used in these notes)
- **GAS**: GNU Assembler (AT&T syntax, part of GCC toolchain)
- **YASM**: Compatible with NASM, supports multiple syntaxes
- **GDB**: GNU Debugger for stepping through assembly
- **objdump**: Disassemble compiled binaries
- **strace**: Trace system calls made by a program

---

## Registers

### General-Purpose Registers

x64 extends x86 registers to 64 bits and adds 8 new registers (R8-R15).

```
64-bit  | 32-bit | 16-bit | 8-bit high | 8-bit low | Purpose
--------|--------|--------|------------|-----------|--------
RAX     | EAX    | AX     | AH         | AL        | Accumulator, return value
RBX     | EBX    | BX     | BH         | BL        | Base (callee-saved)
RCX     | ECX    | CX     | CH         | CL        | Counter, 4th arg
RDX     | EDX    | DX     | DH         | DL        | Data, 3rd arg
RSI     | ESI    | SI     | -          | SIL       | Source index, 2nd arg
RDI     | EDI    | DI     | -          | DIL       | Destination index, 1st arg
RBP     | EBP    | BP     | -          | BPL       | Base pointer (callee-saved)
RSP     | ESP    | SP     | -          | SPL       | Stack pointer
R8      | R8D    | R8W    | -          | R8B       | 5th argument
R9      | R9D    | R9W    | -          | R9B       | 6th argument
R10     | R10D   | R10W   | -          | R10B      | Temporary (caller-saved)
R11     | R11D   | R11W   | -          | R11B      | Temporary (caller-saved)
R12     | R12D   | R12W   | -          | R12B      | Callee-saved
R13     | R13D   | R13W   | -          | R13B      | Callee-saved
R14     | R14D   | R14W   | -          | R14B      | Callee-saved
R15     | R15D   | R15W   | -          | R15B      | Callee-saved
```

```asm
; Accessing different register sizes
mov rax, 0x1122334455667788  ; Full 64-bit
mov eax, 0x55667788          ; Lower 32-bit (zeros upper 32)
mov ax, 0x7788               ; Lower 16-bit
mov ah, 0x77                 ; Bits 8-15
mov al, 0x88                 ; Bits 0-7
```

### Special-Purpose Registers

```
Register | Name              | Purpose
---------|-------------------|----------------------------------
RIP      | Instruction Ptr   | Address of next instruction to execute
RFLAGS   | Flags Register    | Status flags set by operations
RSP      | Stack Pointer     | Points to top of stack
RBP      | Base Pointer      | Frame pointer for stack frames
```

### RFLAGS (Common Flags)

```
Flag | Name      | Set when...
-----|-----------|--------------------------------------------
ZF   | Zero      | Result is zero
SF   | Sign      | Result is negative (MSB = 1)
CF   | Carry     | Unsigned overflow/underflow
OF   | Overflow  | Signed overflow
PF   | Parity    | Low byte has even number of 1-bits
DF   | Direction | String operations go backward
```

---

## Data Types and Memory

### Defining Data

```asm
section .data
    ; Integers
    byte_val   db 42           ; 1 byte  (8-bit)
    word_val   dw 1000         ; 2 bytes (16-bit)
    dword_val  dd 100000       ; 4 bytes (32-bit)
    qword_val  dq 1000000000   ; 8 bytes (64-bit)

    ; Signed values
    neg_byte   db -1           ; 0xFF (two's complement)
    neg_word   dw -1000        ; 0xFC18

    ; Multiple values (arrays)
    numbers    dd 10, 20, 30, 40, 50    ; Array of 5 dwords
    num_count  equ ($ - numbers) / 4    ; Number of elements

    ; Strings
    greeting   db "Hello", 0           ; Null-terminated string
    message    db "Hello, World!", 10, 0  ; With newline and null

    ; Characters
    newline    db 10           ; Newline character
    space      db 32           ; Space character

section .bss
    ; Reserved (uninitialized) space
    buffer     resb 256        ; Reserve 256 bytes
    int_var    resd 1          ; Reserve 1 dword (4 bytes)
    arr_buf    resq 10         ; Reserve 10 qwords (80 bytes)
```

### Size Directives

```asm
; When size is ambiguous, use size specifiers
mov byte  [buffer], 42        ; Store 1 byte
mov word  [buffer], 1000      ; Store 2 bytes
mov dword [buffer], 100000    ; Store 4 bytes
mov qword [buffer], 1000000   ; Store 8 bytes

; Size type summary:
; BYTE  = 1 byte  (8-bit)    db/resb
; WORD  = 2 bytes (16-bit)   dw/resw
; DWORD = 4 bytes (32-bit)   dd/resd
; QWORD = 8 bytes (64-bit)   dq/resq
```

### Endianness

x86-64 is **little-endian**: the least significant byte is stored at the lowest address.

```asm
; Storing 0x12345678 at address 0x1000:
; Address: 0x1000  0x1001  0x1002  0x1003
; Value:   0x78    0x56    0x34    0x12
;          (LSB)                   (MSB)

section .data
    val dd 0x12345678

section .text
    mov eax, [val]       ; EAX = 0x12345678
    mov al, [val]        ; AL = 0x78 (least significant byte)
    mov al, [val + 3]    ; AL = 0x12 (most significant byte)
```

---

## Basic Instructions

### MOV - Data Movement

```asm
; Register to register
mov rax, rbx            ; RAX = RBX

; Immediate to register
mov rax, 42             ; RAX = 42
mov rax, 0xFF           ; RAX = 255
mov rax, 0b1010         ; RAX = 10

; Memory to register
mov rax, [my_var]       ; RAX = value at address my_var
mov rax, [rbx]          ; RAX = value at address in RBX

; Register to memory
mov [my_var], rax       ; Store RAX at address my_var
mov [rbx], rax          ; Store RAX at address in RBX

; CANNOT move memory to memory directly
; mov [dest], [src]     ; ERROR! Use a register as intermediary
mov rax, [src]
mov [dest], rax
```

### LEA - Load Effective Address

```asm
; LEA calculates an address without accessing memory
lea rax, [rbx + rcx*4]      ; RAX = RBX + RCX*4 (address calculation)
lea rax, [rbx + 8]          ; RAX = RBX + 8

; Common use: quick arithmetic
lea rax, [rbx + rbx*2]      ; RAX = RBX * 3
lea rax, [rbx*4 + rbx]      ; RAX = RBX * 5
lea rax, [rax + rax*4]      ; RAX = RAX * 5 (in place)

; Load address of a label
lea rsi, [msg]              ; RSI = address of msg
; vs
mov rsi, msg                ; Same effect with NASM
```

### XCHG, MOVZX, MOVSX

```asm
; XCHG - swap two values
xchg rax, rbx               ; Swap RAX and RBX

; MOVZX - move with zero extension (unsigned)
movzx rax, byte [buffer]    ; Load byte, zero-extend to 64-bit
movzx eax, word [buffer]    ; Load word, zero-extend to 32-bit

; MOVSX - move with sign extension (signed)
movsx rax, byte [buffer]    ; Load byte, sign-extend to 64-bit
movsx eax, word [buffer]    ; Load word, sign-extend to 32-bit

; MOVSXD - sign extend 32-bit to 64-bit
movsxd rax, dword [buffer]
```

### PUSH and POP

```asm
; PUSH - put value on stack (decrements RSP)
push rax                     ; Stack: [RAX] <- RSP
push rbx                     ; Stack: [RBX][RAX] <- RSP
push 42                      ; Push immediate value

; POP - remove value from stack (increments RSP)
pop rbx                      ; RBX = top of stack
pop rax                      ; RAX = next value
```

---

## Arithmetic and Logic

### Arithmetic Operations

```asm
; Addition
add rax, rbx          ; RAX = RAX + RBX
add rax, 10           ; RAX = RAX + 10
add [var], rax        ; [var] = [var] + RAX

; Subtraction
sub rax, rbx          ; RAX = RAX - RBX
sub rax, 10           ; RAX = RAX - 10

; Increment / Decrement
inc rax               ; RAX = RAX + 1
dec rax               ; RAX = RAX - 1

; Negation
neg rax               ; RAX = -RAX (two's complement)

; Multiplication (unsigned)
; MUL multiplies RAX by operand, result in RDX:RAX
mov rax, 10
mov rbx, 3
mul rbx               ; RDX:RAX = RAX * RBX = 30

; Signed multiplication
imul rax, rbx         ; RAX = RAX * RBX (signed, result in RAX)
imul rax, rbx, 5      ; RAX = RBX * 5
imul rax, 10          ; RAX = RAX * 10

; Division (unsigned)
; DIV divides RDX:RAX by operand
; Quotient in RAX, remainder in RDX
mov rax, 17
xor rdx, rdx          ; Clear RDX (important for division!)
mov rbx, 5
div rbx               ; RAX = 3 (quotient), RDX = 2 (remainder)

; Signed division
mov rax, -17
cqo                   ; Sign-extend RAX into RDX:RAX
mov rbx, 5
idiv rbx              ; RAX = -3, RDX = -2
```

### Bitwise Operations

```asm
; AND - bitwise AND
mov rax, 0b1100
and rax, 0b1010       ; RAX = 0b1000 (8)

; OR - bitwise OR
mov rax, 0b1100
or rax, 0b1010        ; RAX = 0b1110 (14)

; XOR - bitwise XOR
mov rax, 0b1100
xor rax, 0b1010       ; RAX = 0b0110 (6)

; NOT - bitwise NOT (flip all bits)
mov rax, 0xFF
not rax               ; RAX = 0xFFFFFFFFFFFFFF00

; Common XOR trick: zero a register
xor rax, rax          ; RAX = 0 (fastest way to zero a register)

; Shift operations
mov rax, 8
shl rax, 2            ; RAX = 32 (shift left = multiply by 2^n)
shr rax, 1            ; RAX = 16 (shift right = divide by 2^n, unsigned)

mov rax, -8
sar rax, 1            ; RAX = -4 (arithmetic shift right, preserves sign)

; Rotate
rol rax, 1            ; Rotate left
ror rax, 1            ; Rotate right
```

### TEST and CMP

```asm
; CMP - compare (performs subtraction, sets flags, discards result)
cmp rax, rbx          ; Sets flags based on RAX - RBX
cmp rax, 10           ; Sets flags based on RAX - 10

; TEST - bitwise AND, sets flags, discards result
test rax, rax         ; Check if RAX is zero (sets ZF)
test rax, 1           ; Check if least significant bit is set (odd/even)

; These are typically followed by conditional jumps (see Control Flow)
```

---

## Control Flow

### Unconditional Jump

```asm
jmp label             ; Jump to label unconditionally

; Example: infinite loop
loop_start:
    ; ... do work ...
    jmp loop_start     ; Jump back to start
```

### Conditional Jumps

```asm
; After CMP or TEST, use conditional jumps:

; Unsigned comparisons
ja   label    ; Jump if above (CF=0 and ZF=0)
jae  label    ; Jump if above or equal (CF=0)
jb   label    ; Jump if below (CF=1)
jbe  label    ; Jump if below or equal (CF=1 or ZF=1)

; Signed comparisons
jg   label    ; Jump if greater
jge  label    ; Jump if greater or equal
jl   label    ; Jump if less
jle  label    ; Jump if less or equal

; Equality
je   label    ; Jump if equal (ZF=1)      (same as JZ)
jne  label    ; Jump if not equal (ZF=0)  (same as JNZ)

; Flag-based
jz   label    ; Jump if zero flag set
jnz  label    ; Jump if zero flag not set
js   label    ; Jump if sign flag set (negative)
jns  label    ; Jump if sign flag not set (positive/zero)
jc   label    ; Jump if carry flag set
jnc  label    ; Jump if carry flag not set
jo   label    ; Jump if overflow
jno  label    ; Jump if no overflow
```

### If-Else Pattern

```asm
; if (rax >= 18) { adult } else { minor }
    cmp rax, 18
    jl .minor           ; Jump if less (signed)

.adult:
    ; ... adult code ...
    jmp .end_if

.minor:
    ; ... minor code ...

.end_if:
    ; ... continue ...
```

### If-ElseIf-Else Pattern

```asm
; Grading: A >= 90, B >= 80, C >= 70, else F
    cmp eax, 90
    jge .grade_a
    cmp eax, 80
    jge .grade_b
    cmp eax, 70
    jge .grade_c
    jmp .grade_f

.grade_a:
    mov bl, 'A'
    jmp .done
.grade_b:
    mov bl, 'B'
    jmp .done
.grade_c:
    mov bl, 'C'
    jmp .done
.grade_f:
    mov bl, 'F'
.done:
```

### Loop Patterns

```asm
; Counting loop (for i = 0; i < 10; i++)
    xor ecx, ecx        ; i = 0
.loop:
    cmp ecx, 10
    jge .loop_end        ; if i >= 10, exit

    ; ... loop body (use ECX as counter) ...

    inc ecx              ; i++
    jmp .loop
.loop_end:

; While loop
.while:
    cmp dword [count], 0
    jle .while_end       ; while (count > 0)

    ; ... loop body ...
    dec dword [count]

    jmp .while
.while_end:

; Do-while loop
.do_loop:
    ; ... loop body ...

    cmp rax, 0
    jne .do_loop         ; } while (rax != 0)

; LOOP instruction (decrements RCX, jumps if RCX != 0)
    mov rcx, 10          ; Loop 10 times
.loop2:
    ; ... loop body ...
    loop .loop2          ; Decrement RCX, jump if not zero
```

---

## The Stack

### Stack Basics

The stack grows **downward** in memory (from high addresses to low).

```asm
; RSP always points to the top of the stack

; Push: decrement RSP, then store
push rax              ; RSP -= 8; [RSP] = RAX

; Pop: load from stack, then increment RSP
pop rax               ; RAX = [RSP]; RSP += 8

; Manual stack manipulation
sub rsp, 32           ; Reserve 32 bytes on stack
; ... use [rsp], [rsp+8], etc. ...
add rsp, 32           ; Clean up (restore RSP)

; Accessing stack values without pop
mov rax, [rsp]        ; Read top of stack without popping
mov rax, [rsp + 8]    ; Read second value on stack
```

### Stack Frame

```asm
; Standard function prologue/epilogue
my_function:
    push rbp              ; Save old base pointer
    mov rbp, rsp          ; Set new base pointer
    sub rsp, 32           ; Reserve local variable space

    ; Local variables:
    ; [rbp - 8]  = first local (8 bytes)
    ; [rbp - 16] = second local (8 bytes)
    ; [rbp - 24] = third local (8 bytes)
    ; [rbp - 32] = fourth local (8 bytes)

    mov qword [rbp - 8], 42    ; first_local = 42

    ; Function body...

    mov rsp, rbp          ; Restore stack pointer
    pop rbp               ; Restore old base pointer
    ret                   ; Return to caller
```

### Stack Alignment

```asm
; The System V AMD64 ABI requires the stack to be 16-byte aligned
; before a CALL instruction. After CALL pushes the return address (8 bytes),
; RSP will be misaligned. Functions must account for this.

; If your function uses an odd number of pushes, you may need:
    sub rsp, 8           ; Align stack to 16 bytes
    ; ... your code ...
    add rsp, 8           ; Restore
```

---

## Functions and Calling Conventions

### System V AMD64 ABI (Linux, macOS)

```
Argument     | Register
-------------|----------
1st integer  | RDI
2nd integer  | RSI
3rd integer  | RDX
4th integer  | RCX
5th integer  | R8
6th integer  | R9
7th+         | Stack (pushed right to left)
Return value | RAX (and RDX for 128-bit)

Caller-saved (volatile):     RAX, RCX, RDX, RSI, RDI, R8-R11
Callee-saved (non-volatile): RBX, RBP, R12-R15, RSP
```

### Writing a Function

```asm
section .text

; int add(int a, int b)
; Arguments: RDI = a, RSI = b
; Returns: RAX = a + b
add_numbers:
    mov rax, rdi          ; RAX = first argument
    add rax, rsi          ; RAX += second argument
    ret                   ; Return (result in RAX)

; int factorial(int n)
; Recursive function
factorial:
    push rbp
    mov rbp, rsp

    cmp rdi, 1            ; if (n <= 1)
    jle .base_case

    push rdi              ; Save n
    dec rdi               ; n - 1
    call factorial        ; factorial(n-1)
    pop rdi               ; Restore n
    imul rax, rdi         ; RAX = n * factorial(n-1)
    jmp .done

.base_case:
    mov rax, 1            ; return 1

.done:
    mov rsp, rbp
    pop rbp
    ret
```

### Calling C Functions

```asm
; Calling printf from assembly
section .data
    fmt db "Hello, %s! You are %d years old.", 10, 0
    name db "Alice", 0

section .text
    extern printf
    global main

main:
    push rbp
    mov rbp, rsp

    ; printf(fmt, name, 25)
    lea rdi, [fmt]        ; 1st arg: format string
    lea rsi, [name]       ; 2nd arg: name
    mov rdx, 25           ; 3rd arg: age
    xor eax, eax          ; AL = 0 (no floating point args)
    call printf

    xor eax, eax          ; Return 0
    mov rsp, rbp
    pop rbp
    ret
```

```bash
# Build with C library linkage
nasm -f elf64 program.asm -o program.o
gcc program.o -o program -no-pie
./program
```

### Inline Assembly in C (GCC)

```c
#include <stdio.h>

int add(int a, int b) {
    int result;
    __asm__ (
        "addl %%ebx, %%eax;"
        : "=a" (result)        // output: result in EAX
        : "a" (a), "b" (b)    // inputs: a in EAX, b in EBX
    );
    return result;
}

int main() {
    printf("5 + 3 = %d\n", add(5, 3));
    return 0;
}
```

---

## Memory Addressing Modes

### Addressing Modes

```asm
; Immediate (constant value)
mov rax, 42                      ; RAX = 42

; Register direct
mov rax, rbx                     ; RAX = RBX

; Direct memory (absolute address)
mov rax, [my_variable]           ; RAX = value at my_variable

; Register indirect
mov rax, [rbx]                   ; RAX = value at address in RBX

; Base + displacement
mov rax, [rbx + 8]               ; RAX = value at RBX + 8

; Base + index
mov rax, [rbx + rcx]             ; RAX = value at RBX + RCX

; Base + index * scale
mov rax, [rbx + rcx*4]           ; RAX = value at RBX + RCX*4
                                  ; Scale can be 1, 2, 4, or 8

; Base + index * scale + displacement
mov rax, [rbx + rcx*8 + 16]     ; RAX = value at RBX + RCX*8 + 16

; RIP-relative (position-independent, used in shared libraries)
mov rax, [rel my_variable]       ; RAX = value at RIP + offset to my_variable
lea rax, [rel my_variable]       ; RAX = address of my_variable
```

### Array Access Patterns

```asm
section .data
    ; Array of 32-bit integers
    numbers dd 10, 20, 30, 40, 50

section .text
    ; Access array[i] where i is in RCX
    lea rbx, [numbers]            ; RBX = base address of array
    mov eax, [rbx + rcx*4]        ; EAX = numbers[RCX] (each element is 4 bytes)

    ; Sequential access
    lea rsi, [numbers]
    mov eax, [rsi]                ; numbers[0] = 10
    mov eax, [rsi + 4]            ; numbers[1] = 20
    mov eax, [rsi + 8]            ; numbers[2] = 30

    ; Loop through array
    lea rsi, [numbers]
    xor ecx, ecx                  ; i = 0
.loop:
    cmp ecx, 5
    jge .done
    mov eax, [rsi + rcx*4]        ; EAX = numbers[i]
    ; ... process element ...
    inc ecx
    jmp .loop
.done:
```

---

## String and Array Operations

### String Instructions

```asm
; REP prefix repeats an instruction RCX times
; Direction Flag (DF): 0 = forward, 1 = backward

section .data
    src db "Hello, World!", 0
    src_len equ $ - src

section .bss
    dest resb 64

section .text
    ; Copy string (like memcpy)
    lea rsi, [src]           ; Source
    lea rdi, [dest]          ; Destination
    mov rcx, src_len         ; Count
    cld                      ; Clear direction flag (forward)
    rep movsb                ; Copy RCX bytes from [RSI] to [RDI]

    ; Fill memory (like memset)
    lea rdi, [dest]          ; Destination
    mov al, 0                ; Fill byte
    mov rcx, 64              ; Count
    rep stosb                ; Store AL at [RDI], RCX times

    ; Compare strings (like memcmp)
    lea rsi, [str1]
    lea rdi, [str2]
    mov rcx, len
    repe cmpsb               ; Compare bytes while equal
    je .strings_equal

    ; Scan for byte (like memchr)
    lea rdi, [buffer]
    mov al, 0                ; Byte to find (null terminator)
    mov rcx, 256             ; Max bytes to scan
    repne scasb              ; Scan until AL found or RCX = 0
    ; RDI now points one past the found byte
    ; RCX contains remaining count
```

### String Length (strlen)

```asm
; Calculate string length
; Input: RDI = pointer to null-terminated string
; Output: RAX = length
my_strlen:
    xor rax, rax             ; length = 0

.loop:
    cmp byte [rdi + rax], 0  ; Check for null terminator
    je .done                 ; If null, we're done
    inc rax                  ; length++
    jmp .loop

.done:
    ret

; Optimized version using REPNE SCASB
my_strlen_fast:
    push rdi
    xor al, al              ; Looking for null byte
    mov rcx, -1              ; Maximum count
    repne scasb              ; Scan forward until null found
    not rcx                  ; RCX = -(count+1), NOT gives count
    dec rcx                  ; Subtract 1 (don't count null)
    mov rax, rcx             ; Return length
    pop rdi
    ret
```

### Array Sum Example

```asm
section .data
    numbers dd 10, 20, 30, 40, 50
    count   equ 5

section .text
    global _start

_start:
    lea rsi, [numbers]       ; Array pointer
    xor eax, eax             ; sum = 0
    xor ecx, ecx             ; i = 0

.sum_loop:
    cmp ecx, count
    jge .done
    add eax, [rsi + rcx*4]  ; sum += numbers[i]
    inc ecx
    jmp .sum_loop

.done:
    ; EAX now contains the sum (150)
    mov edi, eax             ; Exit with sum as exit code
    mov eax, 60              ; sys_exit
    syscall
```

---

## System Calls (Linux)

### Common System Calls

```
RAX | Name      | RDI          | RSI          | RDX           | R10
----|-----------|--------------|--------------|---------------|----
0   | sys_read  | fd           | buffer       | count         |
1   | sys_write | fd           | buffer       | count         |
2   | sys_open  | filename     | flags        | mode          |
3   | sys_close | fd           |              |               |
9   | sys_mmap  | addr         | length       | prot          | flags
12  | sys_brk   | addr         |              |               |
57  | sys_fork  |              |              |               |
59  | sys_execve| filename     | argv         | envp          |
60  | sys_exit  | exit_code    |              |               |
```

### Read from stdin

```asm
section .bss
    buffer resb 256

section .data
    prompt db "Enter your name: ", 0
    prompt_len equ $ - prompt
    greeting db "Hello, ", 0
    greeting_len equ $ - greeting

section .text
    global _start

_start:
    ; Print prompt
    mov rax, 1               ; sys_write
    mov rdi, 1               ; stdout
    lea rsi, [prompt]
    mov rdx, prompt_len
    syscall

    ; Read input
    mov rax, 0               ; sys_read
    mov rdi, 0               ; stdin
    lea rsi, [buffer]
    mov rdx, 255             ; max bytes
    syscall                  ; RAX = bytes read

    mov rbx, rax             ; Save bytes read

    ; Print greeting
    mov rax, 1
    mov rdi, 1
    lea rsi, [greeting]
    mov rdx, greeting_len
    syscall

    ; Print user input
    mov rax, 1
    mov rdi, 1
    lea rsi, [buffer]
    mov rdx, rbx             ; Length from read
    syscall

    ; Exit
    mov rax, 60
    xor rdi, rdi
    syscall
```

### File Operations

```asm
section .data
    filename db "output.txt", 0
    content  db "Hello from assembly!", 10
    content_len equ $ - content

section .text
    global _start

_start:
    ; Open file (create/truncate)
    mov rax, 2               ; sys_open
    lea rdi, [filename]
    mov rsi, 0x241           ; O_WRONLY | O_CREAT | O_TRUNC
    mov rdx, 0o644           ; Permissions: rw-r--r--
    syscall
    mov rbx, rax             ; Save file descriptor

    ; Write to file
    mov rax, 1               ; sys_write
    mov rdi, rbx             ; File descriptor
    lea rsi, [content]
    mov rdx, content_len
    syscall

    ; Close file
    mov rax, 3               ; sys_close
    mov rdi, rbx
    syscall

    ; Exit
    mov rax, 60
    xor rdi, rdi
    syscall
```

---

## Floating Point (SSE/AVX)

### SSE2 Scalar Operations

```asm
section .data
    pi     dq 3.14159265358979    ; 64-bit double
    radius dq 5.0
    two    dq 2.0

section .text
    ; Load doubles into XMM registers
    movsd xmm0, [pi]              ; XMM0 = pi
    movsd xmm1, [radius]          ; XMM1 = radius

    ; Arithmetic
    addsd xmm0, xmm1              ; XMM0 = XMM0 + XMM1
    subsd xmm0, xmm1              ; XMM0 = XMM0 - XMM1
    mulsd xmm0, xmm1              ; XMM0 = XMM0 * XMM1
    divsd xmm0, xmm1              ; XMM0 = XMM0 / XMM1
    sqrtsd xmm0, xmm1             ; XMM0 = sqrt(XMM1)

    ; Circle area: pi * r^2
    movsd xmm0, [pi]
    movsd xmm1, [radius]
    mulsd xmm1, xmm1              ; r^2
    mulsd xmm0, xmm1              ; pi * r^2
    ; Result in XMM0

    ; Comparison
    ucomisd xmm0, xmm1            ; Compare XMM0 with XMM1
    ja .greater                    ; Jump if above

    ; Integer <-> Float conversion
    cvtsi2sd xmm0, rax            ; Integer to double
    cvttsd2si rax, xmm0           ; Double to integer (truncate)

    ; Single precision (32-bit float) uses 'ss' suffix
    movss xmm0, [float_val]
    addss xmm0, xmm1
    cvtss2sd xmm0, xmm0           ; Single to double
```

### Calling C Functions with Floats

```asm
; System V ABI: float args go in XMM0-XMM7
; AL must contain the number of XMM registers used

section .data
    fmt db "Circle area: %.2f", 10, 0
    pi  dq 3.14159265358979
    r   dq 5.0

section .text
    extern printf
    global main

main:
    push rbp
    mov rbp, rsp

    ; Calculate pi * r^2
    movsd xmm0, [pi]
    movsd xmm1, [r]
    mulsd xmm1, xmm1         ; r^2
    mulsd xmm0, xmm1         ; pi * r^2

    ; printf(fmt, area)
    lea rdi, [fmt]            ; 1st arg (string)
    ; xmm0 already has area   ; 1st float arg
    mov al, 1                 ; 1 XMM register used
    call printf

    xor eax, eax
    mov rsp, rbp
    pop rbp
    ret
```

---

## Debugging and Tools

### GDB Commands for Assembly

```bash
# Start debugging
gdb ./program

# Common GDB commands for assembly:
(gdb) break _start          # Set breakpoint at _start
(gdb) run                   # Run the program
(gdb) stepi                 # Step one instruction (si)
(gdb) nexti                 # Step over call (ni)
(gdb) info registers        # Show all registers
(gdb) print $rax            # Print a specific register
(gdb) print/x $rax          # Print in hex
(gdb) x/10x $rsp            # Examine 10 hex values at RSP
(gdb) x/s 0x402000          # Examine as string
(gdb) x/5i $rip             # Disassemble 5 instructions at RIP
(gdb) disassemble           # Disassemble current function
(gdb) set $rax = 42         # Set register value
(gdb) continue              # Continue execution
```

### Useful Tools

```bash
# Disassemble a binary
objdump -d -M intel program

# Show sections
readelf -S program

# Show symbols
nm program

# Trace system calls
strace ./program

# Compile C to assembly (see what the compiler generates)
gcc -S -masm=intel -O2 -o output.s input.c
```

### NASM Debug Macros

```asm
; Print a register value (requires linking with C library)
%macro print_reg 2
    section .data
    %%fmt db %1, ": %lld", 10, 0
    section .text
    push rdi
    push rsi
    push rax
    lea rdi, [%%fmt]
    mov rsi, %2
    xor eax, eax
    call printf
    pop rax
    pop rsi
    pop rdi
%endmacro

; Usage:
print_reg "RAX", rax
print_reg "Counter", rcx
```

---

## Practice Exercises

### Exercise 1: Sum of Array

```asm
; Sum an array of integers and exit with the sum as exit code
section .data
    numbers dd 10, 20, 30, 40, 50
    count   equ 5

section .text
    global _start

_start:
    lea rsi, [numbers]
    xor eax, eax             ; sum = 0
    xor ecx, ecx             ; i = 0

.loop:
    cmp ecx, count
    jge .done
    add eax, [rsi + rcx*4]
    inc ecx
    jmp .loop

.done:
    mov edi, eax             ; Exit code = sum (150)
    mov eax, 60
    syscall
```

### Exercise 2: Integer to String Conversion

```asm
; Convert an integer to a decimal string and print it
section .bss
    buffer resb 32

section .data
    newline db 10

section .text
    global _start

; Convert integer in RAX to string, store at RDI
; Returns: RDI = start of string, RAX = length
int_to_str:
    push rbx
    push rcx
    lea rdi, [buffer + 30]   ; Start from end of buffer
    mov byte [rdi], 0        ; Null terminate
    mov rcx, 10              ; Divisor

    test rax, rax            ; Check if negative
    jns .convert
    neg rax                  ; Make positive (handle sign later)
    push rax
    mov byte [rdi - 1], '-'
    pop rax

.convert:
    xor rdx, rdx
    div rcx                  ; RAX = quotient, RDX = remainder
    add dl, '0'              ; Convert digit to ASCII
    dec rdi
    mov [rdi], dl
    test rax, rax
    jnz .convert

    ; Calculate length
    lea rax, [buffer + 30]
    sub rax, rdi             ; RAX = length

    pop rcx
    pop rbx
    ret

_start:
    mov rax, 12345           ; Number to convert
    call int_to_str

    ; Print the string
    mov rdx, rax             ; Length
    mov rsi, rdi             ; String pointer
    mov rax, 1               ; sys_write
    mov rdi, 1               ; stdout
    syscall

    ; Print newline
    mov rax, 1
    mov rdi, 1
    lea rsi, [newline]
    mov rdx, 1
    syscall

    ; Exit
    mov rax, 60
    xor rdi, rdi
    syscall
```

### Exercise 3: Find Maximum in Array

```asm
section .data
    numbers dd 34, 72, 13, 89, 45, 67, 23, 91, 56, 78
    count   equ 10

section .text
    global _start

_start:
    lea rsi, [numbers]
    mov eax, [rsi]           ; max = numbers[0]
    mov ecx, 1               ; i = 1

.loop:
    cmp ecx, count
    jge .done

    mov edx, [rsi + rcx*4]  ; current = numbers[i]
    cmp edx, eax
    jle .skip
    mov eax, edx             ; max = current

.skip:
    inc ecx
    jmp .loop

.done:
    mov edi, eax             ; Exit with max value (91)
    mov eax, 60
    syscall
```

### Exercise 4: Fibonacci (Using C Library)

```asm
section .data
    fmt db "fib(%d) = %d", 10, 0

section .text
    extern printf
    global main

; int fib(int n) - iterative
; Input: EDI = n
; Output: EAX = fib(n)
fib:
    cmp edi, 1
    jle .base

    xor eax, eax             ; a = 0
    mov ecx, 1               ; b = 1
    mov edx, edi              ; counter = n

.fib_loop:
    cmp edx, 1
    jle .fib_done
    mov esi, ecx              ; temp = b
    add ecx, eax              ; b = a + b
    mov eax, esi              ; a = temp
    dec edx
    jmp .fib_loop

.fib_done:
    mov eax, ecx              ; Return b
    ret

.base:
    mov eax, edi              ; Return n (0 or 1)
    ret

main:
    push rbp
    mov rbp, rsp
    push r12                  ; Callee-saved

    xor r12d, r12d            ; i = 0
.print_loop:
    cmp r12d, 10
    jge .exit

    mov edi, r12d
    call fib

    ; printf(fmt, i, fib(i))
    lea rdi, [fmt]
    mov esi, r12d
    mov edx, eax
    xor eax, eax
    call printf

    inc r12d
    jmp .print_loop

.exit:
    xor eax, eax
    pop r12
    mov rsp, rbp
    pop rbp
    ret
```

```bash
nasm -f elf64 fib.asm -o fib.o
gcc fib.o -o fib -no-pie
./fib
```

---

## Summary

These notes cover the fundamental concepts of x64 assembly programming:

1. **Registers**: 16 general-purpose registers (RAX-R15), RIP, RFLAGS, sub-register access
2. **Data Types**: `db`/`dw`/`dd`/`dq` for bytes/words/dwords/qwords; little-endian storage
3. **Instructions**: `MOV`, `LEA`, `PUSH`/`POP`, `XCHG`, `MOVZX`/`MOVSX`
4. **Arithmetic**: `ADD`, `SUB`, `MUL`/`IMUL`, `DIV`/`IDIV`, `INC`/`DEC`, `NEG`
5. **Bitwise**: `AND`, `OR`, `XOR`, `NOT`, `SHL`/`SHR`/`SAR`, `ROL`/`ROR`
6. **Control Flow**: `CMP`/`TEST`, conditional jumps (`JE`, `JG`, `JL`, etc.), `JMP`, `LOOP`
7. **Stack**: `PUSH`/`POP`, stack frames, 16-byte alignment
8. **Calling Conventions**: System V ABI — arguments in RDI, RSI, RDX, RCX, R8, R9; return in RAX
9. **Addressing Modes**: Immediate, register, direct, indirect, base+index*scale+displacement
10. **Strings**: `REP MOVSB/STOSB/CMPSB/SCASB` for bulk memory operations
11. **System Calls**: Linux `syscall` interface for I/O, files, process control
12. **Floating Point**: SSE2 scalar operations with XMM registers

### Next Steps

1. Practice converting simple C programs to assembly
2. Study compiler output (`gcc -S`) to learn optimization patterns
3. Explore SIMD (SSE/AVX) for parallel data processing
4. Learn about x64 on Windows (different calling convention)
5. Study reverse engineering and binary analysis with tools like Ghidra

### Additional Resources

- **NASM Documentation**: https://www.nasm.us/doc/
- **Intel x86-64 Manuals**: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- **System V ABI**: https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf
- **Linux System Call Table**: https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/
- **x86 Instruction Reference**: https://www.felixcloutier.com/x86/
