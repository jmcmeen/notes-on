# Introduction to GitHub

A comprehensive guide to GitHub, the world's leading platform for version control collaboration, code hosting, and software development workflows.

---

## Table of Contents

- [What is GitHub](#what-is-github)
- [Account Setup](#account-setup)
- [Repository Management](#repository-management)
- [Pull Requests](#pull-requests)
- [Issues](#issues)
- [GitHub CLI](#github-cli)
- [Collaboration](#collaboration)
- [GitHub Pages](#github-pages)
- [Releases](#releases)
- [SSH Keys and Authentication](#ssh-keys-and-authentication)
- [GitHub API Basics](#github-api-basics)
- [Discussions](#discussions)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is GitHub

GitHub is a cloud-based platform built around Git that provides hosting for software development version control. Beyond code hosting, GitHub offers a full suite of collaboration tools including pull requests, issue tracking, project boards, CI/CD with GitHub Actions, and more. Key features:

- **Repository Hosting**: Public and private Git repositories in the cloud
- **Pull Requests**: Structured code review and merge workflow
- **Issues and Projects**: Built-in project management and issue tracking
- **GitHub Actions**: Native CI/CD and automation platform
- **Collaboration**: Teams, organizations, code owners, and branch protection
- **Ecosystem**: Marketplace of integrations, apps, and actions
- **Social Coding**: Stars, forks, followers, and contribution graphs

GitHub supports both open-source communities and enterprise teams, making it the most widely used code hosting platform.

---

## Account Setup

### Creating and Configuring Your Account

```bash
# After creating an account at github.com, configure Git locally
git config --global user.name "Your GitHub Username"
git config --global user.email "your-github-email@example.com"

# Verify your email matches your GitHub account
git config user.email  # Should match the email on your GitHub profile

# Set up credential caching (avoids re-entering password)
git config --global credential.helper cache               # Caches for 15 minutes
git config --global credential.helper 'cache --timeout=3600'  # Cache for 1 hour

# On macOS, use the Keychain
git config --global credential.helper osxkeychain

# On Windows, use the credential manager
git config --global credential.helper manager-core
```

### Two-Factor Authentication

Enabling 2FA is strongly recommended. After enabling 2FA on github.com:

```bash
# HTTPS authentication requires a Personal Access Token (PAT) instead of password
# Generate a PAT at: github.com > Settings > Developer settings > Personal access tokens

# Use the PAT as your password when prompted
git clone https://github.com/user/repo.git
# Username: your-username
# Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  (your PAT)

# Alternatively, use SSH keys (see SSH Keys section below)
```

---

## Repository Management

### Creating Repositories

```bash
# Create a new repository on GitHub via the CLI
gh repo create my-project --public --description "My new project"  # Public repo
gh repo create my-project --private  # Private repo

# Create with a README and license
gh repo create my-project --public --readme --license mit

# Create from an existing local directory
cd my-existing-project
gh repo create --source=. --public --push  # Creates remote and pushes

# Clone a repository from GitHub
git clone https://github.com/user/repo.git       # HTTPS
git clone git@github.com:user/repo.git            # SSH

# Fork a repository (creates your own copy)
gh repo fork owner/repo              # Fork to your account
gh repo fork owner/repo --clone      # Fork and clone locally
gh repo fork owner/repo --remote     # Fork and add as remote
```

### Repository Settings

```bash
# View repository details
gh repo view                    # View current repo info
gh repo view owner/repo         # View any repo info
gh repo view --web              # Open in browser

# Edit repository settings
gh repo edit --description "Updated description"
gh repo edit --visibility public     # Change visibility
gh repo edit --enable-issues         # Enable issues
gh repo edit --enable-wiki           # Enable wiki
gh repo edit --default-branch main   # Set default branch

# List your repositories
gh repo list                        # Your repos
gh repo list --limit 50             # Show more results
gh repo list --language python      # Filter by language
gh repo list owner --source         # Non-forked repos only

# Delete a repository (use with caution)
gh repo delete owner/repo --yes  # Permanently deletes the repo

# Archive a repository
gh repo archive owner/repo  # Makes read-only
```

---

## Pull Requests

### Creating Pull Requests

```bash
# Create a pull request from the current branch
gh pr create --title "Add user authentication" --body "Implements login and signup"

# Create with reviewers and assignees
gh pr create \
  --title "Add search feature" \
  --body "Adds full-text search to the API" \
  --reviewer user1,user2 \
  --assignee @me \
  --label "enhancement"

# Create a draft pull request
gh pr create --draft --title "WIP: Refactor database layer"

# Create from a specific branch to a target branch
gh pr create --base main --head feature/search --title "Add search"

# Create PR and open in browser
gh pr create --fill --web  # Auto-fills from commit messages, opens browser

# Fill PR details from commit messages automatically
gh pr create --fill  # Uses commit messages for title and body
```

### Reviewing Pull Requests

```bash
# List open pull requests
gh pr list                      # All open PRs
gh pr list --state merged       # Merged PRs
gh pr list --label bug          # Filter by label
gh pr list --author user1       # Filter by author
gh pr list --assignee @me       # Assigned to you

# View a specific pull request
gh pr view 42                   # View PR #42
gh pr view 42 --web             # Open PR #42 in browser
gh pr view 42 --comments        # Include comments

# Check out a PR branch locally for testing
gh pr checkout 42               # Switches to the PR branch

# Review a pull request
gh pr review 42 --approve                        # Approve the PR
gh pr review 42 --request-changes --body "Fix the tests"  # Request changes
gh pr review 42 --comment --body "Looks good overall"     # Add a comment

# View PR diff
gh pr diff 42                   # Show the diff for PR #42
```

### Merging Pull Requests

```bash
# Merge a pull request
gh pr merge 42                  # Interactive merge (choose method)
gh pr merge 42 --merge          # Create a merge commit
gh pr merge 42 --squash         # Squash and merge
gh pr merge 42 --rebase         # Rebase and merge

# Merge and delete the branch
gh pr merge 42 --squash --delete-branch  # Squash merge and clean up

# Auto-merge when checks pass
gh pr merge 42 --auto --squash  # Merge automatically when CI passes

# Close a PR without merging
gh pr close 42                  # Close PR #42
gh pr close 42 --comment "Superseded by #45"  # Close with a comment

# Reopen a closed PR
gh pr reopen 42
```

### Code Review Best Practices

```bash
# Check out a PR for local review and testing
gh pr checkout 42
# Run tests locally
npm test  # Or your project's test command

# Leave inline review comments via the web interface
gh pr view 42 --web  # Open in browser for line-by-line comments

# Mark a PR as ready for review (from draft)
gh pr ready 42  # Converts draft PR to ready for review

# View the checks/status for a PR
gh pr checks 42  # Shows CI/CD status for the PR
```

---

## Issues

### Creating and Managing Issues

```bash
# Create a new issue
gh issue create --title "Fix login bug" --body "Users cannot log in with email"

# Create with labels and assignment
gh issue create \
  --title "Add dark mode" \
  --body "Implement dark mode toggle in settings" \
  --label "enhancement,ui" \
  --assignee @me \
  --milestone "v2.0"

# List issues
gh issue list                      # All open issues
gh issue list --state closed       # Closed issues
gh issue list --label bug          # Filter by label
gh issue list --assignee @me       # Assigned to you
gh issue list --milestone "v2.0"   # Filter by milestone

# View an issue
gh issue view 15                   # View issue #15
gh issue view 15 --web             # Open in browser
gh issue view 15 --comments        # Include comments

# Edit an issue
gh issue edit 15 --title "Updated title"
gh issue edit 15 --add-label "priority:high"
gh issue edit 15 --add-assignee user2
gh issue edit 15 --milestone "v2.1"

# Close and reopen issues
gh issue close 15                  # Close issue #15
gh issue close 15 --comment "Fixed in #42"  # Close with comment
gh issue reopen 15                 # Reopen issue #15

# Delete an issue (requires admin access)
gh issue delete 15 --yes
```

### Issue Templates

```bash
# Create an issue template directory
mkdir -p .github/ISSUE_TEMPLATE

# Issue templates are YAML files in .github/ISSUE_TEMPLATE/
# Example: .github/ISSUE_TEMPLATE/bug_report.yml
# ---
# name: Bug Report
# description: File a bug report
# labels: ["bug"]
# body:
#   - type: input
#     id: description
#     attributes:
#       label: Describe the bug
#       placeholder: A clear description of what the bug is
#     validations:
#       required: true
#   - type: textarea
#     id: steps
#     attributes:
#       label: Steps to reproduce
#       placeholder: |
#         1. Go to '...'
#         2. Click on '...'
#         3. See error
```

---

## GitHub CLI

### Installation and Setup

```bash
# Install GitHub CLI on Debian/Ubuntu
sudo apt install gh

# Install on macOS
brew install gh

# Install on Fedora
sudo dnf install gh

# Authenticate with GitHub
gh auth login              # Interactive login (browser or token)
gh auth login --with-token < token.txt  # Login with a PAT from file

# Check authentication status
gh auth status             # Shows current authentication state

# Set default editor and protocol
gh config set editor vim
gh config set git_protocol ssh  # Use SSH for git operations
```

### Common CLI Operations

```bash
# Search repositories
gh search repos "machine learning" --language python --sort stars

# Search issues and PRs across GitHub
gh search issues "memory leak" --repo owner/repo
gh search prs "fix" --state open --repo owner/repo

# View notifications
gh api notifications --jq '.[].subject.title'

# Create a gist
gh gist create file.txt --public --desc "My code snippet"
gh gist create file1.txt file2.txt  # Multi-file gist

# List gists
gh gist list

# Open the current repo in the browser
gh browse                  # Opens repo home page
gh browse --settings       # Opens repo settings
gh browse file.txt         # Opens a specific file
```

---

## Collaboration

### Teams and Permissions

```bash
# Repository permission levels:
# - Read:     Can view and clone the repository
# - Triage:   Can manage issues and PRs (no code push)
# - Write:    Can push to the repository
# - Maintain: Can manage repo settings (no destructive actions)
# - Admin:    Full access including destructive operations

# Add a collaborator to a repository
gh api repos/owner/repo/collaborators/username -X PUT \
  -f permission=write  # Add user with write access

# View collaborators
gh api repos/owner/repo/collaborators --jq '.[].login'
```

### Branch Protection

```bash
# Branch protection rules are typically set via the web UI:
# Settings > Branches > Add rule
# Common protections:
# - Require pull request reviews before merging
# - Require status checks to pass
# - Require signed commits
# - Require linear history
# - Include administrators in restrictions

# Set branch protection via API
gh api repos/owner/repo/branches/main/protection -X PUT \
  -F "required_status_checks[strict]=true" \
  -F "required_status_checks[contexts][]=ci/test" \
  -F "enforce_admins=true" \
  -F "required_pull_request_reviews[required_approving_review_count]=1"
```

### CODEOWNERS

```bash
# Create a CODEOWNERS file to auto-assign reviewers
# Place in the root, docs/, or .github/ directory

# Example .github/CODEOWNERS content:
# * @default-reviewer                    # Default for all files
# *.js @frontend-team                    # JS files reviewed by frontend team
# /docs/ @docs-team                      # Docs directory
# /src/api/ @backend-team @api-lead      # API code
# Dockerfile @devops-team                # Docker files
```

---

## GitHub Pages

### Setting Up GitHub Pages

```bash
# GitHub Pages serves static websites from a repository

# Option 1: Deploy from a branch
# Settings > Pages > Source > Deploy from a branch
# Select main branch, /root or /docs folder

# Option 2: Create a gh-pages branch
git checkout --orphan gh-pages  # Create an empty branch
git rm -rf .                    # Remove all files
echo "<h1>Hello GitHub Pages</h1>" > index.html
git add index.html
git commit -m "Initial GitHub Pages site"
git push origin gh-pages

# View the deployed site URL
gh repo view --json homepageUrl  # If set as homepage

# Your site will be at: https://username.github.io/repo-name/
# For user/org sites: https://username.github.io/ (repo must be named username.github.io)
```

---

## Releases

### Creating and Managing Releases

```bash
# Create a release from a tag
gh release create v1.0.0 --title "Release 1.0.0" --notes "First stable release"

# Create a release with auto-generated notes
gh release create v1.1.0 --generate-notes  # Notes from merged PRs

# Create a draft release
gh release create v2.0.0-beta --draft --prerelease --title "Beta Release"

# Upload release assets
gh release create v1.0.0 ./build/app.zip ./build/app.tar.gz \
  --title "Release 1.0.0" \
  --notes "Download the appropriate archive for your platform"

# List releases
gh release list

# View a specific release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0              # Download all assets
gh release download v1.0.0 -p "*.tar.gz"  # Download matching pattern

# Delete a release
gh release delete v1.0.0 --yes
```

---

## SSH Keys and Authentication

### Setting Up SSH Keys

```bash
# Generate a new SSH key pair
ssh-keygen -t ed25519 -C "your-email@example.com"  # Ed25519 is recommended
# Press Enter to accept default file location (~/.ssh/id_ed25519)
# Enter a passphrase for additional security

# Start the SSH agent
eval "$(ssh-agent -s)"  # Starts the agent in the background

# Add your private key to the SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy the public key to clipboard
cat ~/.ssh/id_ed25519.pub  # Copy this output

# Add the key on GitHub:
# Settings > SSH and GPG keys > New SSH key > Paste your public key

# Test the SSH connection
ssh -T git@github.com  # Should say "Hi username! You've successfully authenticated"

# Switch a repo from HTTPS to SSH
git remote set-url origin git@github.com:user/repo.git
```

### Personal Access Tokens

```bash
# Generate a PAT at: github.com > Settings > Developer settings > Personal access tokens

# Fine-grained tokens (recommended):
# - Scoped to specific repositories
# - Granular permissions per resource type
# - Expiration dates

# Classic tokens:
# - Broader scopes (repo, workflow, admin, etc.)
# - Apply to all accessible repos

# Use a PAT for HTTPS authentication
git clone https://github.com/user/private-repo.git
# When prompted, enter your PAT as the password

# Store PAT using credential helper
echo "https://username:ghp_yourtoken@github.com" | \
  git credential approve  # Stores the credential
```

---

## GitHub API Basics

### Using the GitHub API with gh

```bash
# The gh CLI includes a built-in API client

# Get repository information
gh api repos/owner/repo --jq '.description'

# List repository topics
gh api repos/owner/repo/topics --jq '.names[]'

# Get your user profile
gh api user --jq '{login, name, public_repos}'

# List issues with pagination
gh api repos/owner/repo/issues --paginate --jq '.[].title'

# Create an issue via API
gh api repos/owner/repo/issues -X POST \
  -f title="API-created issue" \
  -f body="Created via the GitHub API"

# GraphQL queries
gh api graphql -f query='
  query {
    viewer {
      login
      repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
        nodes {
          name
          stargazerCount
        }
      }
    }
  }
'

# Get rate limit status
gh api rate_limit --jq '.rate'
```

---

## Discussions

```bash
# GitHub Discussions is a forum-like feature for community conversations
# Enable via: Settings > Features > Discussions (checkbox)
# Categories: Announcements, General, Ideas, Q&A, Show and Tell

# List discussions via API
gh api repos/owner/repo/discussions --jq '.[].title'

# Create a discussion via API
gh api repos/owner/repo/discussions -X POST \
  -f title="Feature request: dark mode" \
  -f body="Would love to see dark mode support" \
  -f category_id="DIC_xxxx"
```

---

## Practice Exercises

### Exercise 1: Repository and Issue Workflow

```bash
# 1. Create a new public repository
gh repo create practice-repo --public --readme --clone
cd practice-repo

# 2. Create an issue
gh issue create --title "Add contributing guidelines" --body "We need a CONTRIBUTING.md"

# 3. Create a branch to address the issue
git checkout -b add-contributing

# 4. Create the file and commit
echo "# Contributing Guidelines" > CONTRIBUTING.md
echo "Please open an issue before submitting a PR." >> CONTRIBUTING.md
git add CONTRIBUTING.md
git commit -m "Add contributing guidelines (closes #1)"

# 5. Push and create a PR
git push -u origin add-contributing
gh pr create --title "Add contributing guidelines" --body "Closes #1"
```

### Exercise 2: Pull Request Review

```bash
# 1. List open PRs in a repository you contribute to
gh pr list

# 2. Check out a PR locally
gh pr checkout 1

# 3. Run tests or review code
git log --oneline -5  # Review the commits

# 4. Leave a review
gh pr review 1 --approve --body "Looks great, approved!"

# 5. Merge the PR
gh pr merge 1 --squash --delete-branch
```

### Exercise 3: Fork and Contribute

```bash
# 1. Fork and clone a repository
gh repo fork owner/interesting-project --clone
cd interesting-project

# 2. Create a branch, make a change, push, and open a PR
git checkout -b fix-typo
git add . && git commit -m "Fix typo in README"
git push -u origin fix-typo
gh pr create --title "Fix typo in README" --body "Fixed a small typo"
```

---

## Summary

GitHub extends Git with powerful collaboration features that form the backbone of modern software development:

- **Repository management**: Creating, forking, cloning, and configuring repos
- **Pull requests**: Structured code review with draft PRs, reviews, and merge strategies
- **Issues**: Full-featured issue tracking with labels, milestones, and templates
- **GitHub CLI**: Command-line access to nearly all GitHub features via `gh`
- **Collaboration**: Teams, permissions, CODEOWNERS, and branch protection rules
- **GitHub Pages**: Free static site hosting from your repository
- **Releases**: Version management with assets and auto-generated notes
- **Authentication**: SSH keys and Personal Access Tokens for secure access
- **API**: REST and GraphQL APIs for automation and integration

---

## Next Steps

- Set up GitHub Actions for CI/CD automation
- Explore GitHub Projects (v2) for project management
- Learn about GitHub Codespaces for cloud development environments
- Set up Dependabot for automated dependency updates
- Explore GitHub Security features (code scanning, secret scanning)

---

## Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Skills (interactive learning)](https://skills.github.com/)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub Community Discussions](https://github.com/orgs/community/discussions)
