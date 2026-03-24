# Introduction to Linux and Unix

## Table of Contents

- [What is Linux and Unix](#what-is-linux-and-unix)
- [Filesystem Hierarchy](#filesystem-hierarchy)
- [Users and Groups](#users-and-groups)
- [File Permissions](#file-permissions)
- [Package Management](#package-management)
- [Process Management](#process-management)
- [Networking](#networking)
- [Disk Management](#disk-management)
- [Environment Variables](#environment-variables)
- [Cron Jobs](#cron-jobs)
- [SSH](#ssh)
- [System Monitoring](#system-monitoring)
- [Text Processing](#text-processing)
- [Service Management with systemd](#service-management-with-systemd)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Linux and Unix

Unix is a family of multitasking, multi-user operating systems originating at AT&T Bell Labs in the 1970s. Linux is a Unix-like kernel created by Linus Torvalds in 1991, which combined with GNU tools forms a complete operating system. Linux is open source, highly configurable, and powers everything from smartphones to the majority of the world's servers.

```bash
# Check the Linux kernel version
uname -r

# Display detailed system information
uname -a

# Show distribution information
cat /etc/os-release

# Display system uptime
uptime
```

Common distributions include Ubuntu/Debian (apt), Red Hat/CentOS/Fedora (yum/dnf), and Arch Linux (pacman).

---

## Filesystem Hierarchy

Linux follows the Filesystem Hierarchy Standard (FHS) with everything organized under the root directory `/`.

```bash
# Key directories:
# /          - Root of the entire filesystem
# /bin       - Essential user binaries (ls, cp, mv)
# /sbin      - Essential system binaries (fdisk, iptables)
# /etc       - System-wide configuration files
# /home      - User home directories
# /root      - Root user's home directory
# /var       - Variable data (logs, mail, spool)
# /var/log   - System and application log files
# /tmp       - Temporary files (often cleared on reboot)
# /usr       - User programs, libraries, documentation
# /usr/local - Locally compiled software
# /opt       - Optional/add-on application packages
# /lib       - Essential shared libraries
# /dev       - Device files
# /proc      - Virtual filesystem for process/kernel info
# /sys       - Virtual filesystem for kernel/device info
# /mnt       - Temporary mount points
# /media     - Mount points for removable media
# /boot      - Boot loader files, kernel images

# View disk usage of top-level directories
du -sh /* 2>/dev/null | sort -rh | head -20
```

### Important Configuration Files

```bash
# Key files in /etc
cat /etc/hostname          # System hostname
cat /etc/hosts             # Static hostname-to-IP mappings
cat /etc/resolv.conf       # DNS resolver configuration
cat /etc/fstab             # Filesystem mount table
cat /etc/passwd            # User account information
cat /etc/group             # Group information
cat /etc/ssh/sshd_config   # SSH daemon configuration
```

---

## Users and Groups

```bash
# View current user and ID information
whoami
id

# List all users on the system
cut -d: -f1 /etc/passwd

# Create a new user with home directory
sudo useradd -m -s /bin/bash newuser

# Set a password
sudo passwd newuser

# Add user to a supplementary group
sudo usermod -aG docker newuser   # -a = append, -G = supplementary group

# Change default shell
sudo usermod -s /bin/zsh newuser

# Lock/unlock a user account
sudo usermod -L newuser           # Lock
sudo usermod -U newuser           # Unlock

# Delete a user and their home directory
sudo userdel -r olduser

# Group management
sudo groupadd developers          # Create group
groups alice                       # View user's groups
sudo gpasswd -d alice developers  # Remove user from group
```

### Understanding /etc/passwd

```bash
# Each line: username:password:UID:GID:comment:home:shell
# Example: alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
# The 'x' means the password is in /etc/shadow

grep "^alice:" /etc/passwd
```

### Sudo

```bash
# Run a command as root
sudo apt update

# Run as a different user
sudo -u postgres psql

# Open a root shell
sudo -i

# Edit sudoers safely (checks syntax)
sudo visudo

# Example sudoers entries:
# alice ALL=(ALL:ALL) ALL                       # Full access
# bob   ALL=(ALL) NOPASSWD: ALL                 # No password prompt
# %developers ALL=(ALL) /usr/bin/systemctl      # Group, limited commands
```

---

## File Permissions

```bash
# Permission types: r(4) w(2) x(1)
# Three sets: owner, group, others
# Example: rwxr-xr-- = 754

# Change permissions
chmod u+x script.sh            # Symbolic: add execute for owner
chmod 755 script.sh            # Octal: rwxr-xr-x
chmod 644 config.yml           # Octal: rw-r--r--
chmod 600 private.key          # Octal: rw-------

# Change ownership
sudo chown alice file.txt                # Owner only
sudo chown alice:developers file.txt     # Owner and group
sudo chown -R alice:alice /home/alice    # Recursive

# Change group
sudo chgrp -R developers project/

# Special permissions
chmod u+s program              # SUID: execute as file owner
chmod g+s shared_dir/          # SGID: new files inherit directory group
chmod +t /tmp/shared           # Sticky bit: only owner can delete files

# View special permissions
ls -l /usr/bin/passwd          # SUID: -rwsr-xr-x
ls -ld /tmp                   # Sticky: drwxrwxrwt
```

---

## Package Management

### Debian/Ubuntu (apt)

```bash
sudo apt update                # Update package index
sudo apt upgrade               # Upgrade installed packages
sudo apt install nginx         # Install a package
sudo apt remove nginx          # Remove (keep config)
sudo apt purge nginx           # Remove with config
sudo apt autoremove            # Remove unused dependencies
apt search "web server"        # Search packages
apt show nginx                 # Package details
```

### Red Hat/CentOS/Fedora (yum/dnf)

```bash
sudo dnf update                # Update all packages
sudo dnf install httpd         # Install a package
sudo dnf remove httpd          # Remove a package
dnf search "web server"        # Search
dnf info httpd                 # Package info
sudo dnf clean all             # Clean cache
# yum uses identical syntax on older systems
```

### Arch Linux (pacman)

```bash
sudo pacman -Syu               # Sync database and upgrade
sudo pacman -S nginx           # Install
sudo pacman -Rns nginx         # Remove with dependencies
pacman -Ss "web server"        # Search
```

---

## Process Management

```bash
# View processes
ps aux                         # All processes with details
ps auxf                        # Process tree format
ps aux --sort=-%cpu | head -10 # Top CPU consumers
ps aux --sort=-%mem | head -10 # Top memory consumers
pgrep nginx                    # Get PID by name

# Interactive monitors
top                            # Real-time process monitor
htop                           # Enhanced monitor (install separately)

# Kill processes
kill 1234                      # SIGTERM: graceful shutdown
kill -9 1234                   # SIGKILL: force kill
killall python3                # Kill all by name
pkill -f "gunicorn"            # Kill by pattern

# Common signals:
# SIGTERM (15) - Graceful termination (default)
# SIGKILL (9)  - Force kill (cannot be caught)
# SIGHUP  (1)  - Reload configuration
```

### systemctl and journalctl

```bash
# Service management
sudo systemctl start nginx     # Start
sudo systemctl stop nginx      # Stop
sudo systemctl restart nginx   # Restart
sudo systemctl reload nginx    # Reload config without restart
systemctl status nginx         # Check status
sudo systemctl enable nginx    # Start at boot
sudo systemctl disable nginx   # Remove from boot

# List services
systemctl list-units --type=service --state=running

# View logs with journalctl
journalctl -u nginx            # Logs for a service
journalctl -u nginx -f         # Follow in real time
journalctl --since "2026-03-24 10:00:00"  # Since a time
journalctl -p err              # Only errors and above
journalctl -b                  # Current boot only
journalctl -n 50               # Last 50 entries
```

---

## Networking

```bash
# Network interfaces and IP addresses
ip addr show                   # All interfaces
ip addr show eth0              # Specific interface
ip route show                  # Routing table
ip route | grep default        # Default gateway

# Diagnostics
ping -c 4 google.com           # Test connectivity
traceroute google.com          # Trace route
nslookup example.com           # DNS lookup
dig example.com                # Detailed DNS lookup

# Active connections
ss -tuln                       # TCP/UDP listening sockets
ss -tunap                      # All connections with process info
netstat -tuln                  # Older alternative to ss

# DNS configuration
cat /etc/resolv.conf           # DNS resolver settings
cat /etc/hosts                 # Static hostname-to-IP mappings
```

### Firewall Basics

```bash
# UFW (Ubuntu/Debian)
sudo ufw status                # Check status
sudo ufw enable                # Enable firewall
sudo ufw allow 22/tcp          # Allow SSH
sudo ufw allow 80/tcp          # Allow HTTP
sudo ufw allow 443/tcp         # Allow HTTPS
sudo ufw deny 3306/tcp         # Block MySQL
sudo ufw allow from 192.168.1.0/24  # Allow subnet
sudo ufw delete allow 80/tcp  # Remove rule

# iptables (all distros)
sudo iptables -L -n            # List rules
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT  # Allow SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT  # Allow HTTP
sudo iptables-save > /etc/iptables/rules.v4          # Persist rules
```

---

## Disk Management

```bash
# Disk space and usage
df -h                          # Filesystem usage
du -sh /var/log                # Directory size
du -sh /var/* 2>/dev/null | sort -rh  # Subdirectory sizes sorted

# Block devices and partitions
lsblk                         # List block devices
sudo fdisk -l                 # Detailed partition info
blkid                         # Filesystem types

# Mount and unmount
sudo mount /dev/sdb1 /mnt/data      # Mount a partition
sudo umount /mnt/data                # Unmount

# Create and check filesystems
sudo mkfs.ext4 /dev/sdb1            # Create ext4 filesystem
sudo fsck /dev/sdb1                 # Check and repair (unmount first)
```

### Persistent Mounts

```bash
# /etc/fstab defines mounts at boot
# Format: device  mount_point  filesystem  options  dump  pass
# /dev/sdb1  /mnt/data  ext4  defaults,noatime  0  2

# Test fstab without rebooting
sudo mount -a
```

---

## Environment Variables

```bash
# View environment variables
env                            # All variables
echo $PATH $HOME $USER         # Specific variables

# Set for current session
export MY_APP_PORT=8080

# Unset a variable
unset MY_APP_PORT

# Add to PATH permanently
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Set for a single command
DB_HOST=localhost DB_PORT=5432 ./start_app.sh
```

---

## Cron Jobs

```bash
# Edit crontab for current user
crontab -e

# List current cron jobs
crontab -l

# Crontab format:
# ┌─────── minute (0-59)
# │ ┌───── hour (0-23)
# │ │ ┌─── day of month (1-31)
# │ │ │ ┌─ month (1-12)
# │ │ │ │ ┌ day of week (0-7, 0 and 7 = Sunday)
# * * * * * command

# Examples:
# 30 2 * * *    /scripts/backup.sh           # Daily at 2:30 AM
# 0 9 * * 1     /scripts/weekly_report.sh    # Mondays at 9 AM
# */15 * * * *  /scripts/healthcheck.sh      # Every 15 minutes
# 0 0 1,15 * *  /scripts/monthly.sh          # 1st and 15th at midnight
# @reboot       /scripts/startup.sh          # At system boot

# Redirect cron output
# * * * * * /scripts/task.sh >> /var/log/task.log 2>&1

# System cron directories: /etc/cron.daily/ /etc/cron.weekly/ /etc/cron.monthly/
```

---

## SSH

```bash
# Connect to a remote server
ssh user@192.168.1.100
ssh -p 2222 user@server.com    # Non-standard port
ssh user@server "df -h"        # Run command remotely

# Generate SSH key pair
ssh-keygen -t ed25519 -C "alice@example.com"

# Copy public key to server (enables passwordless login)
ssh-copy-id user@server.com

# Set correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
```

### SSH Config

```bash
# ~/.ssh/config provides connection shortcuts
# Host myserver
#     HostName 192.168.1.100
#     User alice
#     Port 22
#     IdentityFile ~/.ssh/id_ed25519
#
# Then connect with: ssh myserver
```

### File Transfer

```bash
# SCP
scp file.txt user@server:/home/user/         # Copy to remote
scp user@server:/var/log/app.log ./          # Copy from remote
scp -r ./project/ user@server:/home/user/    # Recursive

# Rsync (efficient, only transfers changes)
rsync -avz ./project/ user@server:/home/user/project/
rsync -avz --delete ./src/ user@server:/deploy/src/  # Mirror
```

---

## System Monitoring

```bash
# Uptime and load averages
uptime
# Load averages (1, 5, 15 min) - compare to number of CPU cores

# Memory usage
free -h

# CPU information
lscpu
nproc                          # Number of CPU cores

# I/O and VM statistics
vmstat 2 5                     # Virtual memory stats (2s interval, 5 samples)
iostat -xz 2 5                 # I/O stats (requires sysstat)

# Find what is using a port
sudo ss -tulnp | grep :80
sudo lsof -i :80

# List open files for a process
sudo lsof -p 1234
```

---

## Text Processing

```bash
# grep: search for patterns
grep "error" /var/log/syslog          # Basic search
grep -i "warning" /var/log/syslog     # Case-insensitive
grep -r "TODO" ./src/                 # Recursive
grep -v "^#" /etc/config              # Exclude lines starting with #
grep -E "error|fail" app.log          # Extended regex (OR)

# sed: stream editor
sed 's/http/https/g' urls.txt         # Replace all
sed -i 's/old/new/g' config.txt       # In-place edit
sed -n '10,20p' file.txt              # Print lines 10-20
sed '/^$/d' file.txt                  # Remove blank lines

# awk: pattern scanning
awk '{print $1}' file.txt             # First column
awk -F: '{print $1, $3}' /etc/passwd  # Custom delimiter
awk '{sum += $1} END {print sum}' nums # Sum column
awk 'NR >= 5 && NR <= 10' file.txt    # Lines 5-10

# Other tools
cut -d: -f1 /etc/passwd               # Extract field
sort file.txt | uniq -c | sort -rn    # Frequency count
echo "hello" | tr 'a-z' 'A-Z'         # Convert case
cat file.txt | tr -d '\r'             # Remove carriage returns
```

---

## Service Management with systemd

```bash
# Common systemctl commands
systemctl status nginx         # View status
sudo systemctl start nginx     # Start
sudo systemctl stop nginx      # Stop
sudo systemctl restart nginx   # Restart
sudo systemctl enable nginx    # Enable at boot
systemctl is-active nginx      # Check if running
systemctl is-enabled nginx     # Check if enabled

# List services
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service

# Reload systemd after modifying unit files
sudo systemctl daemon-reload
```

### Creating a Custom Service

```bash
# Create /etc/systemd/system/myapp.service:
#
# [Unit]
# Description=My Application Server
# After=network.target
#
# [Service]
# Type=simple
# User=appuser
# WorkingDirectory=/opt/myapp
# ExecStart=/opt/myapp/bin/server --port 8080
# Restart=on-failure
# RestartSec=5
# Environment=NODE_ENV=production
#
# [Install]
# WantedBy=multi-user.target

# Then activate:
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
```

---

## Practice Exercises

```bash
# Exercise 1: Create user "developer", group "webteam", add user to group,
# create shared dir /opt/webproject with SGID so files inherit group

# Exercise 2: Write a script logging the date every 10s, create a systemd
# service for it, view logs with journalctl, then stop and disable

# Exercise 3: Check listening ports, configure UFW to allow SSH/HTTP/HTTPS,
# block all other incoming traffic, verify rules

# Exercise 4: Write a disk usage checker that warns if any partition > 80%,
# schedule with cron every hour, log output to /var/log/disk_check.log

# Exercise 5: Analyze /var/log/auth.log with grep/awk/sort/uniq to find
# top 10 messages, count failed SSH attempts, list unique source IPs
```

---

## Summary

Linux and Unix provide a powerful foundation for servers, development, and infrastructure. Key areas covered:

- **Filesystem Hierarchy**: Where things live in the Linux directory tree.
- **Users and Groups**: Managing access through users, groups, and sudo.
- **File Permissions**: Controlling access with rwx, ownership, and special bits.
- **Package Management**: Installing software with apt, dnf, and pacman.
- **Process Management**: Monitoring and controlling processes and services.
- **Networking**: Configuring interfaces, diagnosing issues, managing firewalls.
- **Disk Management**: Monitoring usage, mounting, and managing partitions.
- **Cron Jobs**: Automating tasks on schedules.
- **SSH**: Secure remote access and file transfer.
- **System Monitoring**: Tracking health with uptime, free, vmstat, and more.
- **Text Processing**: Manipulating data with grep, sed, awk, and related tools.
- **systemd**: Managing services, logs, and custom unit files.

---

## Next Steps

- Explore container technologies like Docker and Podman.
- Learn configuration management with Ansible, Puppet, or Chef.
- Study Linux security hardening (SELinux, AppArmor, fail2ban).
- Practice shell scripting for system administration automation.
- Set up web servers (Nginx, Apache) and reverse proxies.
- Learn about namespaces and cgroups, the foundations of containers.

---

## Additional Resources

- [The Linux Documentation Project (TLDP)](https://tldp.org/)
- [Linux man pages online](https://man7.org/linux/man-pages/)
- [ArchWiki](https://wiki.archlinux.org/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Linux Journey](https://linuxjourney.com/)
- [DigitalOcean Community Tutorials](https://www.digitalocean.com/community/tutorials)
