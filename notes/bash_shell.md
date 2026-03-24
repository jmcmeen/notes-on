# Introduction to Bash and Shell Scripting

## Table of Contents

- [What is Bash](#what-is-bash)
- [Shell Basics](#shell-basics)
- [Navigation and File Management](#navigation-and-file-management)
- [File Content and Text Processing](#file-content-and-text-processing)
- [File Permissions](#file-permissions)
- [Redirection and Pipes](#redirection-and-pipes)
- [Variables and Environment](#variables-and-environment)
- [Script Basics](#script-basics)
- [Control Flow](#control-flow)
- [Loops](#loops)
- [Functions](#functions)
- [Arrays](#arrays)
- [String Manipulation](#string-manipulation)
- [Process Management](#process-management)
- [Useful Commands](#useful-commands)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Bash

Bash (Bourne Again SHell) is a command-line interpreter and scripting language that serves as the default shell on most Linux distributions and macOS. It was created by Brian Fox in 1989 as a free replacement for the Bourne Shell (sh).

```bash
# Check which shell you are currently using
echo $SHELL

# Check the Bash version installed
bash --version

# List all available shells on the system
cat /etc/shells
```

---

## Shell Basics

The shell takes commands from the keyboard and gives them to the operating system to perform. A terminal emulator is the window that provides access to the shell.

```bash
# Clear the terminal screen
clear

# Basic command structure: command [options] [arguments]
ls -la /home

# Run multiple commands on one line
echo "Hello"; echo "World"

# Run second command only if the first succeeds
mkdir mydir && cd mydir

# Run second command only if the first fails
cd mydir || mkdir mydir
```

### Getting Help

```bash
# View the manual page for a command
man ls

# Search man pages by keyword
man -k "copy files"

# Show a short description
whatis cp

# Built-in help for shell builtins
help cd

# Most commands support --help
grep --help
```

### Command History

```bash
# View command history
history

# Re-run the last command
!!

# Re-run command number 42
!42

# Search history interactively with Ctrl + R
```

---

## Navigation and File Management

```bash
# Print the current working directory
pwd

# Change directories
cd ~              # Home directory
cd /var/log       # Absolute path
cd ..             # Up one level
cd -              # Previous directory

# List files and directories
ls                # Basic listing
ls -a             # Include hidden files
ls -la            # Detailed with hidden files
ls -lh            # Human-readable sizes
ls -lt            # Sort by modification time

# Create directories
mkdir projects
mkdir -p projects/webapp/src    # Create nested directories

# Copy files and directories
cp source.txt dest.txt          # Copy a file
cp -r src/ backup_src/          # Copy directory recursively

# Move or rename
mv old_name.txt new_name.txt
mv report.pdf ~/Documents/

# Remove files and directories
rm file.txt                     # Remove a file
rm -r old_project               # Remove directory recursively
rm -rf temp_build               # Force remove without prompts

# Find files
find /home -name "*.log"        # Find by name
find . -iname "readme*"         # Case-insensitive
find . -mtime -7                # Modified in last 7 days
find . -name "*.tmp" -exec rm {} \;  # Find and execute

# Locate files using indexed database
locate nginx.conf
sudo updatedb                   # Update the locate database
```

---

## File Content and Text Processing

```bash
# Display file contents
cat file.txt                    # Entire file
cat -n file.txt                 # With line numbers

# View beginning and end of files
head -n 20 file.txt             # First 20 lines
tail -n 50 file.txt             # Last 50 lines
tail -f /var/log/syslog         # Follow in real time

# Page through a file interactively
less large_file.log             # q to quit, / to search

# Search with grep
grep "error" logfile.txt        # Basic search
grep -i "warning" logfile.txt   # Case-insensitive
grep -r "TODO" ./src/           # Recursive search
grep -n "function" script.js    # Show line numbers
grep -v "DEBUG" app.log         # Invert match (exclude)
grep -c "error" logfile.txt     # Count matches
grep -E "error|warning" app.log # Extended regex

# Count, sort, filter
wc -l file.txt                  # Count lines
sort names.txt                  # Sort alphabetically
sort -n numbers.txt             # Sort numerically
sort data.txt | uniq -c         # Count unique occurrences
cut -d',' -f1,3 data.csv       # Extract columns

# awk and sed
awk '{print $2}' file.txt              # Print second column
awk -F',' '{print $1, $3}' data.csv   # Custom delimiter
awk '{sum += $1} END {print sum}' nums # Sum a column
sed 's/old/new/g' file.txt             # Replace all occurrences
sed -i 's/old/new/g' file.txt          # In-place edit
sed '/^#/d' config.txt                 # Delete comment lines
```

---

## File Permissions

```bash
# View permissions
ls -l
# Example: -rwxr-xr-- 1 john developers 4096 Mar 24 10:00 script.sh
#          |___|___|__|
#          owner group others

# Change permissions with chmod
chmod u+x script.sh        # Add execute for owner
chmod go-w file.txt         # Remove write for group and others
chmod 755 script.sh         # rwxr-xr-x (executable)
chmod 644 file.txt          # rw-r--r-- (standard file)
chmod 600 secret.key        # rw------- (private file)
chmod -R 755 /var/www/html/ # Recursive

# Change ownership
sudo chown alice file.txt             # Change owner
sudo chown alice:developers file.txt  # Change owner and group
chgrp developers file.txt             # Change group only
sudo chown -R www-data:www-data /var/www/  # Recursive

# Umask controls default permissions for new files
umask              # Display current umask
umask 022          # New files: 644, new dirs: 755
umask 027          # New files: 640, new dirs: 750
```

---

## Redirection and Pipes

```bash
# Redirect stdout to a file
echo "Hello" > output.txt      # Overwrite
echo "More" >> output.txt      # Append

# Redirect stdin from a file
sort < unsorted.txt

# Redirect stderr
command_that_fails 2> error.log

# Redirect both stdout and stderr
command &> all_output.log

# Discard output
command > /dev/null 2>&1

# Pipes: send output of one command as input to another
ls -l | grep ".txt"
cat access.log | grep "404" | sort | uniq -c | sort -rn | head -10

# Tee: write to file AND pass to next command
ls -la | tee file_list.txt | grep ".sh"

# Here document: multi-line input
cat <<EOF
Line one with variable: $HOME
Line two
EOF

# Here string
grep "pattern" <<< "search in this string"
```

---

## Variables and Environment

```bash
# Assign a variable (no spaces around =)
name="Alice"
echo "Hello, $name"
echo "File: ${name}_report.txt"   # Curly braces for clarity

# Command substitution
today=$(date +%Y-%m-%d)

# Arithmetic
result=$((5 * 3 + 2))

# Environment variables
echo $HOME $USER $PATH $PWD $SHELL

# Export for child processes
export MY_APP_ENV="production"

# Add to PATH
export PATH="$HOME/bin:$PATH"

# Startup files:
# ~/.bashrc       - Interactive non-login shells
# ~/.bash_profile - Login shells
# /etc/profile    - System-wide login shell settings

# Reload .bashrc
source ~/.bashrc
```

---

## Script Basics

```bash
#!/bin/bash
# The shebang line tells the system to use Bash
# Make executable: chmod +x myscript.sh
# Run: ./myscript.sh or bash myscript.sh

echo "Script name: $0"         # Script's own name
echo "First argument: $1"      # First positional argument
echo "All arguments: $@"       # All arguments as separate words
echo "Argument count: $#"      # Number of arguments

# Exit codes: 0 = success, non-zero = failure
ls /nonexistent 2>/dev/null
echo "Exit code: $?"

# Exit with error
if [ -z "$1" ]; then
    echo "Error: No argument provided" >&2
    exit 1
fi
exit 0
```

```bash
#!/bin/bash
# Strict mode: exit on errors, undefined variables, pipe failures
set -euo pipefail

# Debug mode: trace each command
set -x
```

---

## Control Flow

```bash
#!/bin/bash
# If/elif/else
age=25
if [ "$age" -lt 18 ]; then
    echo "Minor"
elif [ "$age" -lt 65 ]; then
    echo "Adult"
else
    echo "Senior"
fi

# Numeric: -eq -ne -lt -le -gt -ge
# String:  = != -z (empty) -n (non-empty)
# File:    -f (file) -d (dir) -e (exists) -r -w -x

# Double brackets support pattern and regex matching
if [[ "$filename" == *.txt ]]; then
    echo "Text file"
fi

if [[ "$email" =~ ^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$ ]]; then
    echo "Valid email"
fi

# Case statement
case "$fruit" in
    apple) echo "Red or green" ;;
    banana) echo "Yellow" ;;
    orange|tangerine) echo "Citrus" ;;
    *) echo "Unknown" ;;
esac
```

---

## Loops

```bash
#!/bin/bash
# For loop over values
for color in red green blue; do
    echo "Color: $color"
done

# For loop over files
for file in *.log; do
    wc -l "$file"
done

# C-style for loop
for ((i = 0; i < 5; i++)); do
    echo "Index: $i"
done

# Range with step
for i in {0..100..10}; do
    echo "$i"
done

# While loop
count=1
while [ "$count" -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < input.txt

# Until loop: runs until condition becomes true
attempts=0
until [ "$attempts" -ge 3 ]; do
    attempts=$((attempts + 1))
done

# Break and continue
for i in {1..10}; do
    [ $((i % 2)) -eq 0 ] && continue  # Skip even numbers
    echo "Odd: $i"
done
```

---

## Functions

```bash
#!/bin/bash
# Define and call a function
greet() {
    echo "Hello, $1!"     # $1 is the first argument to the function
}
greet "Alice"

# Return values (exit codes)
is_even() {
    [ $(($1 % 2)) -eq 0 ] && return 0 || return 1
}
if is_even 4; then echo "Even"; fi

# Capture output with command substitution
get_timestamp() { date +"%Y-%m-%d %H:%M:%S"; }
current_time=$(get_timestamp)

# Local variables prevent polluting global scope
calculate() {
    local result=$(($1 + $2))
    echo "$result"
}
sum=$(calculate 10 20)
```

---

## Arrays

```bash
#!/bin/bash
# Indexed array
fruits=("apple" "banana" "cherry")
echo "${fruits[0]}"        # First element
echo "${fruits[@]}"        # All elements
echo "${#fruits[@]}"       # Count

fruits+=("date")           # Append

for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# Associative arrays (Bash 4+)
declare -A capitals
capitals[France]="Paris"
capitals[Germany]="Berlin"

for country in "${!capitals[@]}"; do
    echo "$country -> ${capitals[$country]}"
done
```

---

## String Manipulation

```bash
#!/bin/bash
str="Hello, World!"
echo "${#str}"             # Length: 13
echo "${str:7:5}"          # Substring: World
echo "${str/World/Bash}"   # Replace first match

filename="archive.tar.gz"
echo "${filename#*.}"      # Remove shortest front match: tar.gz
echo "${filename##*.}"     # Remove longest front match: gz
echo "${filename%.*}"      # Remove shortest back match: archive.tar
echo "${filename%%.*}"     # Remove longest back match: archive

echo "${undefined:-default}"  # Default if unset

name="alice"
echo "${name^^}"           # ALICE (uppercase)
echo "${name^}"            # Alice (capitalize first)
```

---

## Process Management

```bash
# View running processes
ps aux                        # All processes with details
ps aux | grep nginx           # Find specific process

# Interactive monitors
top                           # Real-time process viewer

# Kill processes
kill 1234                     # SIGTERM (graceful)
kill -9 1234                  # SIGKILL (force)
killall nginx                 # Kill by name
pkill -f "python app.py"     # Kill by pattern

# Background and foreground jobs
long_command &                # Run in background
jobs                          # List background jobs
fg %1                         # Bring to foreground
bg %1                         # Resume in background
# Ctrl+Z suspends a foreground process

# Survive terminal closure
nohup ./script.sh > output.log 2>&1 &

# Wait for background processes
wait                          # Wait for all
wait $!                       # Wait for most recent
```

---

## Useful Commands

```bash
# Archives
tar -czvf archive.tar.gz directory/    # Create compressed archive
tar -xzvf archive.tar.gz              # Extract archive
tar -xzvf archive.tar.gz -C /opt/     # Extract to specific dir

# Download files
curl -O https://example.com/file.tar.gz         # Save with original name
curl -o output.txt https://example.com/data      # Custom name
curl -s https://api.example.com/data | jq '.'    # Silent + pipe to jq
wget https://example.com/file.tar.gz             # Download with wget

# SSH
ssh user@192.168.1.100                 # Connect to remote server
ssh -p 2222 user@server.com            # Custom port
ssh user@remote "df -h && free -m"     # Run remote command
ssh-keygen -t ed25519 -C "email@example.com"  # Generate key pair
ssh-copy-id user@server.com            # Copy public key to server

# SCP: secure copy
scp file.txt user@remote:/home/user/   # Copy to remote
scp user@remote:/var/log/app.log ./    # Copy from remote
scp -r dir/ user@remote:/backup/       # Copy directory

# xargs: pass output as arguments
find . -name "*.log" | xargs rm
find . -name "*.tmp" -print0 | xargs -0 rm  # Handle spaces
cat urls.txt | xargs -I {} curl -O {}        # Per-line execution
cat servers.txt | xargs -P 4 -I {} ssh {} "uptime"  # Parallel
```

---

## Practice Exercises

```bash
# Exercise 1: Write a script that organizes files in a directory
# into subdirectories by their extension (.txt, .log, .csv, etc.)

# Exercise 2: Write a log analyzer that reads a web server log and reports
# total requests, top 10 URLs, 404 count, and requests per hour

# Exercise 3: Write a backup script that creates timestamped tar.gz archives,
# removes backups older than 30 days, and logs all actions

# Exercise 4: Write a system health check that warns if disk > 80%,
# reports memory and CPU load, and checks if critical services are running

# Exercise 5: Write a batch renamer that replaces spaces with underscores,
# converts to lowercase, and adds a date prefix to filenames
```

---

## Summary

Bash and shell scripting form the backbone of working with Unix-like systems. The key concepts covered include:

- **Shell Basics**: Interacting with the terminal, man pages, and command history.
- **File Management**: Navigating directories, creating/removing files, and finding files.
- **Text Processing**: Viewing, searching, and transforming content with grep, awk, and sed.
- **Permissions**: Controlling access with chmod, chown, and umask.
- **Redirection and Pipes**: Connecting commands and controlling I/O streams.
- **Scripting**: Writing scripts with variables, control flow, loops, functions, and arrays.
- **Process Management**: Running, monitoring, and controlling processes.
- **Utility Commands**: Archiving, downloading, transferring, and remote connections.

---

## Next Steps

- Learn about traps, signals, and process substitution.
- Study regular expressions in depth for advanced text processing.
- Explore shell scripting best practices (Google Shell Style Guide).
- Practice automation scripts for real-world tasks.
- Learn alternative shells like Zsh and Fish.
- Move on to configuration management tools like Ansible.

---

## Additional Resources

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Advanced Bash-Scripting Guide (TLDP)](https://tldp.org/LDP/abs/html/)
- [ShellCheck - Shell Script Linter](https://www.shellcheck.net/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ExplainShell.com](https://explainshell.com/)
- [The Linux Command Line (Book by William Shotts)](https://linuxcommand.org/tlcl.php)
