# Introduction to Windows Administration

## Table of Contents

- [What is Windows](#what-is-windows)
- [PowerShell Basics](#powershell-basics)
- [File System Navigation](#file-system-navigation)
- [Environment Variables](#environment-variables)
- [Package Management](#package-management)
- [Windows Subsystem for Linux](#windows-subsystem-for-linux)
- [PowerShell Scripting](#powershell-scripting)
- [Services](#services)
- [Registry Basics](#registry-basics)
- [Task Scheduler](#task-scheduler)
- [Networking](#networking)
- [Remote Management](#remote-management)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Windows

Windows is Microsoft's operating system used broadly in enterprise environments and development workstations. From a developer and DevOps perspective, Windows provides PowerShell as a powerful automation framework, Windows Subsystem for Linux (WSL2) for running Linux tools natively, and tight integration with Azure cloud services.

```powershell
# Check Windows version and build
Get-ComputerInfo | Select-Object WindowsVersion, OsBuildNumber, OsArchitecture

# Check PowerShell version
$PSVersionTable
```

---

## PowerShell Basics

PowerShell is an object-oriented shell built on .NET. Unlike Bash which passes text, PowerShell passes structured objects through the pipeline.

### Cmdlets and Help

```powershell
# Cmdlets follow Verb-Noun naming: Get-Process, Set-Location, New-Item

# Get help for a cmdlet
Get-Help Get-Process -Examples

# Find commands by keyword
Get-Command *process*

# Find commands by verb or noun
Get-Command -Verb Get
Get-Command -Noun Service
```

### Pipelines and Object Manipulation

```powershell
# PowerShell passes objects through pipes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Select specific properties
Get-Process | Select-Object Name, CPU, WorkingSet

# Filter with Where-Object
Get-Process | Where-Object { $_.CPU -gt 100 }

# Iterate with ForEach-Object
Get-Service | ForEach-Object { Write-Output "$($_.Name): $($_.Status)" }

# Group and measure
Get-Process | Group-Object ProcessName | Sort-Object Count -Descending
Get-Process | Measure-Object WorkingSet -Sum -Average

# Format and export
Get-Process | Format-Table Name, CPU, WorkingSet -AutoSize
Get-Process | Export-Csv -Path "processes.csv" -NoTypeInformation
Get-Process | Select-Object Name, CPU | ConvertTo-Json
```

### Common Aliases

```powershell
# Built-in aliases for familiar commands
# ls -> Get-ChildItem    cd -> Set-Location    pwd -> Get-Location
# cp -> Copy-Item        mv -> Move-Item       rm  -> Remove-Item
# cat -> Get-Content     echo -> Write-Output   cls -> Clear-Host

Get-Alias                      # View all aliases
```

---

## File System Navigation

```powershell
# Current directory
Get-Location

# Change directory
Set-Location C:\Users\john\Documents

# List files and directories
Get-ChildItem                  # Basic listing
Get-ChildItem -Force           # Include hidden files
Get-ChildItem -Recurse -Filter "*.log"  # Recursive search

# Create files and directories
New-Item -ItemType Directory -Path "C:\Projects\webapp"
New-Item -ItemType File -Path "config.json"
Set-Content -Path "hello.txt" -Value "Hello, World!"

# Copy, move, remove
Copy-Item -Path "source.txt" -Destination "backup.txt"
Copy-Item -Path ".\project" -Destination ".\backup" -Recurse
Move-Item -Path "old.txt" -Destination "new.txt"
Remove-Item -Path ".\old_project" -Recurse -Force

# Read file content
Get-Content -Path "logfile.txt"
Get-Content -Path "logfile.txt" -Tail 20     # Last 20 lines
Get-Content -Path "logfile.txt" -Wait -Tail 10  # Follow like tail -f
```

---

## Environment Variables

```powershell
# View all environment variables
Get-ChildItem Env:

# Get specific variables
$env:PATH
$env:USERNAME
$env:COMPUTERNAME
$env:USERPROFILE

# Set for current session
$env:MY_APP_ENV = "development"

# Remove a variable
Remove-Item Env:\MY_APP_ENV

# Set persistent user-level variable
[System.Environment]::SetEnvironmentVariable("MY_VAR", "value", "User")

# Set persistent machine-level variable (requires admin)
[System.Environment]::SetEnvironmentVariable("MY_VAR", "value", "Machine")

# Add to PATH permanently
$currentPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
[System.Environment]::SetEnvironmentVariable("PATH", "$currentPath;C:\mytools", "User")

# PowerShell variables (not environment variables)
$myVar = "Hello"
Get-Variable myVar
Set-Variable -Name "myVar" -Value "Updated"
```

```powershell
# Open environment variable editor GUI
rundll32 sysdm.cpl,EditEnvironmentVariables
```

---

## Package Management

### winget

```powershell
# Search and install
winget search "visual studio code"
winget install Microsoft.VisualStudioCode
winget install --id Git.Git -e --silent   # Silent install

# List and manage
winget list                    # Installed packages
winget upgrade --all           # Upgrade all packages
winget uninstall Microsoft.VisualStudioCode

# Export/import package lists
winget export -o packages.json
winget import -i packages.json
```

### Chocolatey

```powershell
# Install packages (-y auto-confirms)
choco install git -y
choco install nodejs python3 docker-desktop -y

# Manage packages
choco list --local-only        # List installed
choco upgrade all -y           # Upgrade all
choco uninstall git -y         # Remove
```

### Scoop

```powershell
# Scoop installs per-user, no admin required
scoop bucket add extras        # Add a package bucket
scoop install git              # Install
scoop list                     # List installed
scoop update *                 # Update all
scoop search nodejs            # Search
```

---

## Windows Subsystem for Linux

WSL2 runs a full Linux kernel alongside Windows with near-native performance.

### Installation and Setup

```powershell
# Install WSL2 with default Ubuntu (run as Administrator)
wsl --install

# Install a specific distribution
wsl --install -d Ubuntu-22.04

# List available and installed distributions
wsl --list --online
wsl --list --verbose

# Set WSL2 as default version
wsl --set-default-version 2

# Manage WSL instances
wsl                            # Start default distro
wsl --shutdown                 # Shut down all instances
wsl --terminate Ubuntu-22.04   # Terminate specific distro
```

### WSL Integration

```bash
# Access Windows files from WSL
ls /mnt/c/Users/john/Documents

# Run Windows executables from WSL
explorer.exe .
notepad.exe myfile.txt
```

```powershell
# Run Linux commands from PowerShell
wsl ls -la /home

# Access WSL files from Windows (via \\wsl$\)
Get-ChildItem "\\wsl$\Ubuntu\home\john"

# Open WSL folder in VS Code
wsl code /home/john/project
```

### WSL Configuration

```bash
# /etc/wsl.conf inside the distribution:
# [automount]
# enabled = true
# root = /mnt/
#
# [network]
# generateHosts = true
# generateResolvConf = true
#
# [boot]
# systemd = true          # Enable systemd (WSL 0.67.6+)
#
# [user]
# default = john
```

---

## PowerShell Scripting

### Variables and Data Types

```powershell
# Variables
$name = "Alice"
$age = 30
$isAdmin = $true
$items = @("apple", "banana", "cherry")   # Array
$config = @{                               # Hashtable
    Host = "localhost"
    Port = 8080
    Debug = $false
}

# Access hashtable values
$config.Host
$config["Port"]
```

### Control Flow

```powershell
# If/ElseIf/Else
$score = 85
if ($score -ge 90) {
    Write-Output "Grade: A"
} elseif ($score -ge 80) {
    Write-Output "Grade: B"
} else {
    Write-Output "Grade: F"
}

# Operators: -eq -ne -gt -ge -lt -le -like -match -contains

# Switch statement
switch ($day) {
    "Monday"  { Write-Output "Start of week" }
    "Friday"  { Write-Output "Almost weekend" }
    default   { Write-Output "Midweek" }
}
```

### Loops

```powershell
# ForEach
foreach ($fruit in @("apple", "banana", "cherry")) {
    Write-Output "Fruit: $fruit"
}

# For loop
for ($i = 0; $i -lt 5; $i++) {
    Write-Output "Index: $i"
}

# While loop
$count = 1
while ($count -le 5) {
    Write-Output "Count: $count"
    $count++
}
```

### Functions

```powershell
# Basic function with default parameter
function Get-Greeting {
    param ([string]$Name = "World")
    return "Hello, $Name!"
}
Get-Greeting -Name "Alice"

# Advanced function with validation
function New-Backup {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,

        [string]$DestinationPath = "C:\Backups",

        [ValidateSet("Full", "Incremental")]
        [string]$Type = "Full"
    )

    if (-not (Test-Path $DestinationPath)) {
        New-Item -ItemType Directory -Path $DestinationPath | Out-Null
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $backupName = "backup_${Type}_${timestamp}.zip"
    $fullPath = Join-Path $DestinationPath $backupName

    Compress-Archive -Path $SourcePath -DestinationPath $fullPath
    Write-Verbose "Backup created: $fullPath"
    return $fullPath
}
```

---

## Services

```powershell
# List and filter services
Get-Service
Get-Service | Where-Object { $_.Status -eq "Running" }
Get-Service -Name "wuauserv"
Get-Service -DisplayName "*SQL*"

# Start, stop, restart
Start-Service -Name "wuauserv"
Stop-Service -Name "wuauserv"
Restart-Service -Name "wuauserv"

# Configure startup type
Set-Service -Name "wuauserv" -StartupType Automatic
Set-Service -Name "wuauserv" -StartupType Manual
Set-Service -Name "wuauserv" -StartupType Disabled

# Using sc.exe
sc.exe query "wuauserv"                          # Query status
sc.exe config "wuauserv" start=auto              # Set startup
sc.exe create "MyService" binPath="C:\app\svc.exe" start=auto  # Create
```

---

## Registry Basics

The Windows Registry is a hierarchical database storing OS and application configuration.

```powershell
# Navigate like a filesystem
Set-Location HKLM:\SOFTWARE\Microsoft

# List registry keys
Get-ChildItem HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion

# Read values
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" -Name "ProductName"

# Create and set values
New-Item -Path "HKCU:\Software\MyApp"
New-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Version" -Value "1.0" -PropertyType String
Set-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting1" -Value "Enabled"

# Remove
Remove-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Version"
Remove-Item -Path "HKCU:\Software\MyApp" -Recurse

# Hives: HKLM: (Machine), HKCU: (User), HKCR: (Classes Root)
```

---

## Task Scheduler

```powershell
# List scheduled tasks
Get-ScheduledTask

# Create a daily task at 2 AM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File C:\Scripts\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "2:00AM"

Register-ScheduledTask -TaskName "DailyBackup" `
    -Action $action -Trigger $trigger `
    -Description "Daily backup" -User "SYSTEM"

# Manage tasks
Start-ScheduledTask -TaskName "DailyBackup"     # Run now
Disable-ScheduledTask -TaskName "DailyBackup"   # Disable
Enable-ScheduledTask -TaskName "DailyBackup"    # Enable
Unregister-ScheduledTask -TaskName "DailyBackup" -Confirm:$false  # Remove
```

---

## Networking

```powershell
# IP configuration
ipconfig /all
Get-NetIPAddress | Where-Object { $_.InterfaceAlias -eq "Ethernet" }

# DNS
ipconfig /flushdns
Resolve-DnsName example.com

# Connections and testing
netstat -ano                   # Active connections with PIDs
Test-Connection -ComputerName google.com -Count 4       # Ping
Test-NetConnection -ComputerName server.com -Port 443   # Port test

# Routing and adapters
Get-NetRoute
Get-NetAdapter

# Firewall
Get-NetFirewallRule | Where-Object { $_.Enabled -eq "True" } | Select-Object Name, Direction, Action

New-NetFirewallRule -DisplayName "Allow Port 8080" `
    -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

Remove-NetFirewallRule -DisplayName "Allow Port 8080"
```

---

## Remote Management

```powershell
# Enable remoting on target (run as Administrator)
Enable-PSRemoting -Force

# Interactive remote session
Enter-PSSession -ComputerName server01 -Credential (Get-Credential)

# Run commands remotely
Invoke-Command -ComputerName server01 -ScriptBlock {
    Get-Service | Where-Object { $_.Status -eq "Running" }
} -Credential (Get-Credential)

# Run on multiple machines
$servers = @("server01", "server02", "server03")
Invoke-Command -ComputerName $servers -ScriptBlock {
    hostname; Get-Date
}

# Persistent session for multiple commands
$session = New-PSSession -ComputerName server01
Invoke-Command -Session $session -ScriptBlock { $env:COMPUTERNAME }
Remove-PSSession $session
```

### SSH from Windows

```powershell
# Windows 10+ includes OpenSSH client
ssh user@192.168.1.100
ssh-keygen -t ed25519 -C "john@example.com"
scp .\deploy.ps1 user@server:/home/user/scripts/

# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

---

## Practice Exercises

```powershell
# Exercise 1: Write a system inventory script collecting computer name,
# OS version, RAM, disk space, running services, and top 10 processes
# by memory. Export to CSV and HTML.

# Exercise 2: Write a file cleanup script that finds files older than
# N days, logs them, prompts for confirmation, then deletes.
# Schedule with Task Scheduler.

# Exercise 3: Write a service monitor that checks a list of services,
# restarts stopped ones, and logs all actions with timestamps.

# Exercise 4: Set up WSL2 with Ubuntu, install dev tools (git, Node.js,
# Python), configure shared SSH keys between Windows and WSL.

# Exercise 5: Use Invoke-Command to collect uptime, disk space, and
# event log errors from multiple remote machines. Generate an HTML report.
```

---

## Summary

Windows administration has evolved to embrace command-line and automation-first approaches. Key concepts covered:

- **PowerShell**: Object-oriented shell with cmdlets, pipelines, and filtering.
- **File Management**: Navigating and manipulating files with PowerShell cmdlets.
- **Environment Variables**: Managing session and persistent variables.
- **Package Management**: Installing software with winget, Chocolatey, and Scoop.
- **WSL2**: Running Linux alongside Windows for cross-platform development.
- **Scripting**: Variables, control flow, loops, and functions in PowerShell.
- **Services**: Managing Windows services programmatically.
- **Registry**: Accessing and modifying system configuration.
- **Task Scheduler**: Automating recurring tasks.
- **Networking**: Diagnosing issues and managing firewall rules.
- **Remote Management**: Administering machines with PowerShell remoting and SSH.

---

## Next Steps

- Learn PowerShell Desired State Configuration (DSC).
- Explore Windows Server roles: Active Directory, IIS, DNS.
- Study Group Policy for managing environments at scale.
- Learn about Windows containers with Docker Desktop.
- Explore Azure integration and Azure PowerShell modules.

---

## Additional Resources

- [Microsoft PowerShell Documentation](https://learn.microsoft.com/en-us/powershell/)
- [PowerShell Gallery](https://www.powershellgallery.com/)
- [WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [Windows Terminal Documentation](https://learn.microsoft.com/en-us/windows/terminal/)
- [Chocolatey Documentation](https://docs.chocolatey.org/)
- [SS64 PowerShell Reference](https://ss64.com/ps/)
