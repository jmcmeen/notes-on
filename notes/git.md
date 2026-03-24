# Introduction to Git

A comprehensive guide to Git version control, covering everything from basic concepts to advanced workflows and techniques.

---

## Table of Contents

- [What is Git](#what-is-git)
- [Installation and Setup](#installation-and-setup)
- [Repository Basics](#repository-basics)
- [Staging and Committing](#staging-and-committing)
- [Branching](#branching)
- [Remote Repositories](#remote-repositories)
- [Merge Conflicts](#merge-conflicts)
- [Git Log and History](#git-log-and-history)
- [Undoing Changes](#undoing-changes)
- [Tags](#tags)
- [Gitignore](#gitignore)
- [Git Workflows](#git-workflows)
- [Interactive Rebase](#interactive-rebase)
- [Cherry-pick](#cherry-pick)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Git

Git is a distributed version control system (DVCS) created by Linus Torvalds in 2005 for Linux kernel development. Unlike centralized systems such as SVN, every developer's working copy is a full repository with complete history and version-tracking capabilities.

Key characteristics of Git:

- **Distributed**: Every clone is a full backup of the repository
- **Speed**: Most operations are performed locally
- **Data Integrity**: Every file and commit is checksummed with SHA-1
- **Branching**: Lightweight branching and merging support
- **Staging Area**: An intermediate area to craft commits precisely

Git tracks content as snapshots, not differences. Each commit stores a snapshot of all tracked files at that point in time, with pointers to unchanged files from prior commits.

---

## Installation and Setup

### Installing Git

```bash
# Install Git on Debian/Ubuntu
sudo apt update
sudo apt install git

# Install Git on Fedora/RHEL
sudo dnf install git

# Install Git on macOS via Homebrew
brew install git

# Verify installation
git --version  # Should display something like "git version 2.43.0"
```

### Initial Configuration

```bash
# Set your identity (required for commits)
git config --global user.name "Your Name"       # Your full name
git config --global user.email "you@example.com" # Your email address

# Set the default branch name for new repositories
git config --global init.defaultBranch main  # Use "main" instead of "master"

# Set your preferred text editor
git config --global core.editor "vim"   # Options: vim, nano, code --wait, etc.

# Enable colorized output for readability
git config --global color.ui auto

# Set line ending behavior
git config --global core.autocrlf input  # Use "true" on Windows, "input" on macOS/Linux

# View all configuration settings
git config --list           # Lists all active config settings
git config --global --list  # Lists only global settings

# View a specific config value
git config user.name  # Displays the currently set user name
```

### Configuration Levels

```bash
# System-level config (applies to all users)
git config --system core.editor "vim"  # Stored in /etc/gitconfig

# Global config (applies to current user)
git config --global user.name "John"   # Stored in ~/.gitconfig

# Local config (applies to current repository only)
git config --local user.email "work@company.com"  # Stored in .git/config
```

---

## Repository Basics

### Initializing a Repository

```bash
# Create a new directory and initialize it as a Git repository
mkdir my-project
cd my-project
git init  # Creates a .git directory with repository metadata

# Initialize a bare repository (used for remote/server repos)
git init --bare my-project.git  # No working directory, only .git contents
```

### Cloning a Repository

```bash
# Clone a remote repository via HTTPS
git clone https://github.com/user/repo.git  # Downloads entire repo history

# Clone via SSH (requires SSH key setup)
git clone git@github.com:user/repo.git

# Clone into a specific directory
git clone https://github.com/user/repo.git my-folder  # Custom folder name

# Shallow clone (only recent history, faster for large repos)
git clone --depth 1 https://github.com/user/repo.git  # Only the latest commit

# Clone a specific branch
git clone --branch develop https://github.com/user/repo.git  # Checks out "develop"
```

### Repository Structure

```bash
# View the .git directory contents
ls -la .git/
# Key contents:
#   HEAD        - Points to the current branch reference
#   config      - Repository-specific configuration
#   objects/    - Stores all content (blobs, trees, commits)
#   refs/       - Stores branch and tag pointers
#   hooks/      - Client-side and server-side scripts
#   index       - The staging area information
```

---

## Staging and Committing

### The Three States

Files in Git exist in three main states:

1. **Modified**: Changed but not staged
2. **Staged**: Marked to go into the next commit
3. **Committed**: Safely stored in the local database

### Checking Status

```bash
# Show the current state of the working directory and staging area
git status          # Full output with instructions
git status -s       # Short format: M=modified, A=added, ??=untracked
git status --branch # Include branch and tracking info
```

### Staging Changes

```bash
# Stage a specific file
git add index.html  # Adds index.html to the staging area

# Stage multiple files
git add file1.txt file2.txt  # Add specific files

# Stage all changes in the current directory
git add .  # Stages new, modified, and deleted files

# Stage all changes in the entire repository
git add -A  # Same as git add --all

# Stage parts of a file interactively
git add -p  # Lets you choose hunks to stage from each file

# Remove a file from staging (unstage)
git restore --staged file.txt  # Keeps changes in working directory
```

### Viewing Differences

```bash
# Show unstaged changes (working directory vs staging area)
git diff              # Displays line-by-line differences

# Show staged changes (staging area vs last commit)
git diff --staged     # What will be included in the next commit

# Compare branches and files
git diff main..feature  # Changes between main and feature branches
git diff -- file.txt    # Limit diff output to one file
git diff --stat         # Shows files changed, insertions, deletions
```

### Committing Changes

```bash
# Commit staged changes with a message
git commit -m "Add navigation bar to homepage"  # Inline commit message

# Open editor for detailed commit message
git commit  # Opens configured editor for the message

# Stage and commit all tracked modified files in one step
git commit -a -m "Update all configuration files"  # Skips untracked files

# Amend the most recent commit (change message or add files)
git add forgotten-file.txt
git commit --amend -m "Updated commit message"  # Replaces the last commit

# Create an empty commit (useful for triggering CI)
git commit --allow-empty -m "Trigger CI pipeline"
```

---

## Branching

### Branch Basics

```bash
# List branches
git branch         # Local branches (current marked with *)
git branch -a      # All branches (local and remote)

# Create and switch to a new branch
git checkout -b feature-login  # Traditional way
git switch -c feature-login    # Modern way (Git 2.23+)

# Switch to an existing branch
git checkout main    # Traditional way
git switch main      # Modern way

# Rename and delete branches
git branch -m old-name new-name  # Rename a branch
git branch -d feature-login     # Safe delete (only if merged)
git branch -D feature-login     # Force delete (even if not merged)
```

### Merging

```bash
# Merge a branch into the current branch
git checkout main              # Switch to the target branch first
git merge feature-login        # Merge feature-login into main

# No fast-forward merge (always creates a merge commit)
git merge --no-ff feature-login  # Preserves branch history

# Squash merge (combines all commits into one)
git merge --squash feature-login  # Stages changes but does not commit
git commit -m "Add login feature"  # You commit manually

# Abort a merge in progress
git merge --abort  # Reverts to the state before merge started
```

### Rebasing

```bash
# Rebase current branch onto main
git checkout feature-login
git rebase main  # Replays feature-login commits on top of main

# Continue, abort, or skip during rebase
git rebase --continue  # After fixing conflicts and staging changes
git rebase --abort     # Return to state before rebase
git rebase --skip      # Drop the current conflicting commit
```

---

## Remote Repositories

### Managing Remotes

```bash
# View configured remotes
git remote         # Lists remote names
git remote -v      # Lists names with fetch and push URLs

# Add a remote repository
git remote add origin https://github.com/user/repo.git  # "origin" is conventional
git remote add upstream https://github.com/original/repo.git  # For forks

# Change a remote's URL
git remote set-url origin git@github.com:user/repo.git  # Switch to SSH

# Rename or remove a remote
git remote rename origin primary  # Rename "origin" to "primary"
git remote remove upstream        # Delete the remote reference
```

### Fetching, Pulling, and Pushing

```bash
# Fetch changes from remote (download without merging)
git fetch origin         # Fetch all branches from origin
git fetch --all          # Fetch from all configured remotes
git fetch --prune        # Remove local references to deleted remote branches

# Pull changes (fetch + merge)
git pull origin main          # Fetch and merge main from origin
git pull --rebase origin main # Fetch and rebase instead of merge

# Push changes to remote
git push origin main             # Push main branch to origin
git push -u origin feature-login # Push and set upstream tracking
git push origin --tags           # Push all tags

# Delete a remote branch
git push origin --delete feature-login  # Remove branch from remote

# Force push (use with extreme caution)
git push --force-with-lease origin main  # Safer than --force, checks for updates
```

### Tracking Branches

```bash
# Set upstream tracking for the current branch
git branch --set-upstream-to=origin/main  # Track origin/main

# View tracking information
git branch -vv  # Shows tracking relationships and ahead/behind counts
```

---

## Merge Conflicts

### Understanding Conflicts

Merge conflicts occur when Git cannot automatically resolve differences between two branches. This happens when both branches modify the same lines in a file.

### Resolving Conflicts

```bash
# When a merge produces conflicts:
git merge feature-branch
# Output: CONFLICT (content): Merge conflict in file.txt

# Conflicted files contain markers:
# <<<<<<< HEAD
# Your changes on the current branch
# =======
# Changes from the branch being merged
# >>>>>>> feature-branch

# After manually editing the file to resolve conflicts:
git add file.txt       # Mark the conflict as resolved
git commit             # Complete the merge

# Use a merge tool for visual conflict resolution
git mergetool          # Opens configured merge tool
```

### Conflict Prevention Tips

```bash
# Regularly sync with the main branch to reduce divergence
git checkout feature-branch
git merge main  # Or: git rebase main

# Pull before pushing to catch conflicts early
git pull origin main

# Use smaller, focused branches to minimize overlapping changes
# Keep branches short-lived and merge frequently
```

---

## Git Log and History

### Viewing Commit History

```bash
# Basic log output
git log            # Shows commit hash, author, date, and message
git log --oneline  # Abbreviated hash and first line of message

# Show commit graph with branch visualization
git log --oneline --graph --all  # ASCII art of branch topology

# Limit and filter results
git log -5                     # Show only the last 5 commits
git log --since="2024-01-01"   # Commits since a date
git log --author="John"        # Commits by authors matching "John"
git log --grep="fix"           # Commits with "fix" in the message

# Show changes in each commit
git log -p            # Full diff of each commit
git log --stat        # Summary of files changed per commit

# Custom format
git log --pretty=format:"%h %an %ar - %s"  # Hash, author, relative date, subject
```

### Inspecting Specific Commits

```bash
# Show details of a specific commit
git show abc1234  # Displays the commit metadata and diff

# Show a file at a specific commit
git show abc1234:path/to/file.txt  # Contents of file at that commit

# Show who last modified each line of a file
git blame file.txt            # Annotates each line with commit info
git blame -L 10,20 file.txt   # Blame only lines 10-20
git blame -w file.txt         # Ignore whitespace changes
```

### Bisect (Finding Bugs)

```bash
# Binary search to find which commit introduced a bug
git bisect start
git bisect bad               # Mark current commit as bad (has the bug)
git bisect good abc1234      # Mark a known good commit
# Git checks out a commit halfway between; test, then mark:
git bisect good              # If this commit does not have the bug
git bisect bad               # If this commit has the bug
# Repeat until Git identifies the first bad commit
git bisect reset             # End the session, return to original branch

# Automated bisect with a test script
git bisect start && git bisect bad HEAD && git bisect good abc1234
git bisect run ./test-script.sh  # Exit 0=good, non-zero=bad
```

---

## Undoing Changes

### Restore (Working Directory and Staging)

```bash
# Discard changes in the working directory (restore to last commit)
git restore file.txt       # Reverts file.txt to the committed version
git restore .              # Discard all unstaged changes

# Unstage a file (remove from staging area)
git restore --staged file.txt  # File remains modified in working directory

# Restore a file to a specific commit's version
git restore --source=abc1234 file.txt  # Gets file from that commit
```

### Reset

```bash
# Soft reset (moves HEAD, keeps changes staged)
git reset --soft HEAD~1  # Undo last commit, changes remain staged

# Mixed reset (moves HEAD, unstages changes - default)
git reset HEAD~1         # Undo last commit, changes in working directory

# Hard reset (moves HEAD, discards all changes)
git reset --hard HEAD~1       # Completely undo last commit and all changes
git reset --hard origin/main  # Match local to remote exactly
```

### Revert

```bash
# Create a new commit that undoes a previous commit (safe, no history rewrite)
git revert abc1234              # Reverts the specified commit
git revert --no-commit abc1234  # Stage the revert without committing
git revert -m 1 abc1234        # Revert a merge commit (-m 1 = mainline parent)
```

### Stash

```bash
# Save uncommitted changes to the stash
git stash                                    # Stashes staged and unstaged changes
git stash push -m "Work in progress"         # Stash with a descriptive message
git stash -u                                 # Also stash untracked files

# List and apply stashes
git stash list                   # Shows stash@{0}, stash@{1}, etc.
git stash apply                  # Re-apply most recent stash (keeps in list)
git stash pop                    # Apply and remove from stash list
git stash apply stash@{2}       # Apply a specific stash entry

# Remove stashes
git stash drop stash@{0}        # Remove a specific stash entry
git stash clear                  # Remove all stash entries permanently

# Create a branch from a stash
git stash branch new-branch stash@{0}  # Applies stash to a new branch
```

---

## Tags

```bash
# List tags
git tag              # Alphabetical list
git tag -l "v1.*"    # Filter tags matching a pattern

# Create tags
git tag v1.0.0                                 # Lightweight tag (just a pointer)
git tag -a v1.0.0 -m "Release version 1.0.0"  # Annotated tag (recommended)
git tag -a v0.9.0 abc1234 -m "Beta release"   # Tag a past commit

# Push and delete tags
git push origin v1.0.0              # Push a specific tag
git push origin --tags              # Push all tags
git tag -d v1.0.0                   # Delete locally
git push origin --delete v1.0.0    # Delete from remote

# Checkout a tag (detached HEAD state)
git checkout v1.0.0  # Working directory matches that tag
```

---

## Gitignore

### Creating and Using .gitignore

```bash
# Create a .gitignore file in the repository root
# Common .gitignore patterns:
# *.pyc                  # Compiled files
# __pycache__/
# node_modules/          # Dependency directories
# venv/
# dist/                  # Build output
# build/
# .vscode/               # IDE files
# .idea/
# .DS_Store              # OS files
# .env                   # Secrets and environment
# *.pem
# *.log                  # Log files
# !important.log         # Negate a pattern (include despite prior rule)
```

### Global Gitignore and Tracked File Removal

```bash
# Set a global gitignore for all repositories
git config --global core.excludesfile ~/.gitignore_global

# Remove a file that is already tracked (stop tracking without deleting)
git rm --cached file.txt  # Removes from Git but keeps on disk

# Check if a file is ignored and why
git check-ignore -v file.txt  # Shows which rule causes the ignore
```

---

## Git Workflows

### Feature Branch Workflow

```bash
# 1. Start from an up-to-date main branch
git checkout main
git pull origin main

# 2. Create a feature branch
git checkout -b feature/user-authentication

# 3. Work on the feature (edit, stage, commit)
git add .
git commit -m "Add user login endpoint"
git commit -m "Add password validation"

# 4. Push the feature branch to remote
git push -u origin feature/user-authentication

# 5. Create a pull request on GitHub/GitLab (via web UI or CLI)

# 6. After review, merge into main
git checkout main
git merge feature/user-authentication
git push origin main

# 7. Clean up the feature branch
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### GitFlow Workflow

```bash
# Main branches: main (production), develop (integration)
# Supporting branches: feature/*, release/*, hotfix/*

# Start and finish a feature
git checkout develop
git checkout -b feature/shopping-cart
# ... work on feature ...
git checkout develop
git merge --no-ff feature/shopping-cart  # Always create a merge commit
git branch -d feature/shopping-cart

# Create a release (merge to main and develop, then tag)
git checkout develop
git checkout -b release/1.0.0
# Bump version numbers, fix bugs, then:
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git checkout develop
git merge --no-ff release/1.0.0
git branch -d release/1.0.0

# Hotfix (urgent fix from production, merge to main and develop)
git checkout main
git checkout -b hotfix/fix-login-crash
# Fix the bug, then:
git checkout main
git merge --no-ff hotfix/fix-login-crash
git tag -a v1.0.1 -m "Hotfix 1.0.1"
git checkout develop
git merge --no-ff hotfix/fix-login-crash
git branch -d hotfix/fix-login-crash
```

### Trunk-Based Development

```bash
# All developers work on short-lived branches off main (1-2 days max)
git checkout main && git pull origin main
git checkout -b short-feature

# Make small, incremental commits and rebase frequently
git add . && git commit -m "Add input validation helper"
git fetch origin && git rebase origin/main

# Merge back quickly via pull request
git push -u origin short-feature
# Create PR, get quick review, merge, delete branch
```

---

## Interactive Rebase

```bash
# Rebase the last N commits interactively
git rebase -i HEAD~4  # Opens editor with last 4 commits

# Available commands in the editor:
# pick   - Use the commit as-is
# reword - Edit the commit message
# squash - Combine with previous commit (keeps both messages)
# fixup  - Combine with previous commit (discards this message)
# drop   - Remove the commit entirely

# Example: Squash the last 3 commits into one
git rebase -i HEAD~3
# Change "pick" to "squash" for the 2nd and 3rd commits, save, edit message

# Edit a past commit
git rebase -i HEAD~3
# Change "pick" to "edit", make changes, then:
git add .
git commit --amend
git rebase --continue  # Proceed with remaining commits

# Abort an interactive rebase
git rebase --abort  # Returns to the original state
```

---

## Cherry-pick

```bash
# Apply a specific commit from another branch to the current branch
git cherry-pick abc1234  # Applies the commit as a new commit

# Cherry-pick without committing (stage only)
git cherry-pick --no-commit abc1234  # Lets you modify before committing

# Cherry-pick a range of commits
git cherry-pick abc1234..def5678  # Excludes abc1234, includes def5678
git cherry-pick abc1234^..def5678  # Includes both endpoints

# Handle conflicts during cherry-pick
git cherry-pick abc1234
# If conflicts arise:
git add .                   # Stage resolved files
git cherry-pick --continue  # Complete the cherry-pick

# Abort a cherry-pick
git cherry-pick --abort  # Cancel and return to original state
```

---

## Practice Exercises

### Exercise 1: Repository Setup and Basic Workflow

```bash
# 1. Create a new project directory and initialize Git
mkdir git-practice && cd git-practice
git init

# 2. Configure local user info
git config --local user.name "Practice User"
git config --local user.email "practice@example.com"

# 3. Create a file, stage it, and make your first commit
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit with README"

# 4. Create a .gitignore file and commit it
echo "*.log" > .gitignore
echo "node_modules/" >> .gitignore
git add .gitignore
git commit -m "Add .gitignore"
```

### Exercise 2: Branching and Merging

```bash
# 1. Create a feature branch and add commits
git checkout -b feature/add-docs
echo "## Installation" >> README.md
git add README.md && git commit -m "Add installation section"
echo "## Usage" >> README.md
git add README.md && git commit -m "Add usage section"

# 2. Merge back to main and clean up
git checkout main
git merge --no-ff feature/add-docs -m "Merge feature/add-docs"
git branch -d feature/add-docs
git log --oneline --graph --all  # View the result
```

---

## Summary

Git is the foundation of modern software development collaboration. The key concepts covered in this guide include:

- **Repository basics**: Initializing, cloning, and understanding the .git structure
- **Staging and committing**: The three states of files, precise commit crafting
- **Branching**: Creating, switching, merging, and rebasing branches
- **Remote repositories**: Connecting to remotes, fetching, pulling, and pushing
- **Conflict resolution**: Understanding and resolving merge conflicts
- **History inspection**: Logs, blame, show, and bisect for debugging
- **Undoing changes**: Restore, reset, revert, and stash for flexible recovery
- **Tags and releases**: Marking important points in history
- **Workflows**: Feature branch, GitFlow, and trunk-based development patterns
- **Advanced techniques**: Interactive rebase and cherry-pick for history management

---

## Next Steps

- Practice daily Git usage on personal or open-source projects
- Learn about Git hooks for automating tasks (pre-commit, pre-push)
- Explore Git submodules and subtrees for multi-repo management
- Study GitHub or GitLab specific features (pull requests, CI/CD)
- Learn about signed commits with GPG keys and Git LFS for binary assets

---

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [Pro Git Book (free)](https://git-scm.com/book/en/v2)
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (interactive)](https://learngitbranching.js.org/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
