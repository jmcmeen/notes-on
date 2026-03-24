# Introduction to GitHub Actions

A comprehensive guide to GitHub Actions, GitHub's built-in CI/CD and automation platform for building, testing, and deploying code directly from your repositories.

---

## Table of Contents

- [What is GitHub Actions](#what-is-github-actions)
- [Core Concepts](#core-concepts)
- [Workflow Files](#workflow-files)
- [Actions](#actions)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Matrix Strategy](#matrix-strategy)
- [Caching](#caching)
- [Artifacts](#artifacts)
- [Conditional Execution](#conditional-execution)
- [Reusable Workflows](#reusable-workflows)
- [Common CI/CD Patterns](#common-cicd-patterns)
- [Docker Container Actions](#docker-container-actions)
- [Self-Hosted Runners](#self-hosted-runners)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is GitHub Actions

GitHub Actions is a CI/CD and workflow automation platform integrated directly into GitHub. It allows you to automate tasks triggered by repository events such as pushes, pull requests, releases, and scheduled times. Key advantages:

- **Native Integration**: Built into GitHub with no external service needed
- **Event-Driven**: Trigger workflows from any GitHub event
- **Marketplace**: Thousands of pre-built actions available
- **Matrix Builds**: Test across multiple versions and platforms simultaneously
- **Flexibility**: Supports Linux, macOS, and Windows runners

---

## Core Concepts

### Workflows, Events, Jobs, Steps, and Runners

- **Workflow**: An automated process defined in a YAML file, triggered by events
- **Event**: A trigger that starts a workflow (push, pull_request, schedule, etc.)
- **Job**: A set of steps that run on the same runner; jobs run in parallel by default
- **Step**: An individual task within a job (runs a command or an action)
- **Runner**: The server that executes the workflow (GitHub-hosted or self-hosted)

```yaml
# Basic structure of a workflow file
# File: .github/workflows/ci.yml
name: CI Pipeline          # Name displayed in the Actions tab

on: push                   # Event that triggers this workflow

jobs:                       # One or more jobs to execute
  build:                    # Job identifier (user-defined name)
    runs-on: ubuntu-latest  # Runner environment
    steps:                  # Ordered list of steps
      - uses: actions/checkout@v4  # Step 1: Check out repository code
      - name: Run tests            # Step 2: Execute a command
        run: echo "Running tests"  # Shell command to run
```

---

## Workflow Files

### YAML Syntax and Structure

Workflow files must be placed in the `.github/workflows/` directory of your repository.

```yaml
# File: .github/workflows/main.yml
name: Main Workflow

on:
  push:
    branches: [main, develop]        # Only trigger on these branches
    paths: ['src/**', 'tests/**']    # Only when these paths change
    paths-ignore: ['**.md']          # Ignore changes to these paths

  pull_request:
    branches: [main]                  # PRs targeting main branch

  schedule:
    - cron: '0 6 * * 1'              # Run at 6:00 AM UTC every Monday

  workflow_dispatch:                   # Allow manual triggering from the UI
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]

  release:
    types: [published]                # Trigger when a release is published

jobs:
  build:
    name: Build and Test
    runs-on: ubuntu-latest            # GitHub-hosted runner
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4     # Check out repository code
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci                   # Clean install from lockfile
      - run: npm run lint             # Run linting
      - run: npm test                 # Run test suite
```

### Multiple Event Triggers

```yaml
# Trigger on tag pushes
on:
  push:
    tags:
      - 'v*.*.*'     # Matches tags like v1.0.0, v2.1.3
```

---

## Actions

### Using Marketplace Actions

```yaml
# Actions are reusable units of code referenced with "uses"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4                # Check out code
      - uses: actions/setup-python@v5            # Setup Python
        with:
          python-version: '3.12'
          cache: 'pip'                           # Cache pip dependencies
      - uses: actions/setup-java@v4              # Setup Java
        with:
          distribution: 'temurin'
          java-version: '21'
      - uses: actions/setup-go@v5                # Setup Go
        with:
          go-version: '1.22'
```

### Creating Custom Composite Actions

```yaml
# File: .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Install dependencies and configure the project'
inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20'

runs:
  using: 'composite'                    # Composite action type
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - name: Install dependencies
      run: npm ci
      shell: bash                       # Required for composite actions
```

```yaml
# Using the custom action in a workflow
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-project  # Reference local action
        with:
          node-version: '20'
      - run: npm test
```

---

## Environment Variables and Secrets

### Environment Variables

```yaml
# Set environment variables at different scopes
env:
  APP_ENV: production          # Workflow-level variable (available to all jobs)

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: postgres://localhost/mydb  # Job-level variable

    steps:
      - name: Print environment
        env:
          STEP_VAR: "hello"    # Step-level variable
        run: |
          echo "App env: $APP_ENV"           # Access workflow variable
          echo "DB URL: $DATABASE_URL"       # Access job variable
          echo "Step var: $STEP_VAR"         # Access step variable

      - name: Use GitHub context variables
        run: |
          echo "Repository: ${{ github.repository }}"  # owner/repo
          echo "Branch: ${{ github.ref_name }}"         # Branch or tag name
          echo "SHA: ${{ github.sha }}"                 # Full commit SHA
          echo "Actor: ${{ github.actor }}"             # User who triggered
```

### Secrets

```yaml
# Secrets are set in: Settings > Secrets and variables > Actions
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        env:
          SSH_KEY: ${{ secrets.SSH_PRIVATE_KEY }}  # Access a secret
        run: |
          echo "$SSH_KEY" > key.pem && chmod 600 key.pem
          ssh -i key.pem user@server "deploy.sh"
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

```bash
# Set secrets via the GitHub CLI
gh secret set API_TOKEN --body "your-secret-value"    # Repository secret
gh secret set DB_PASSWORD --env production             # Environment secret
```

---

## Matrix Strategy

```yaml
# Run jobs across multiple configurations simultaneously
jobs:
  test:
    runs-on: ${{ matrix.os }}           # Dynamic runner selection
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]  # Three OS options
        node-version: [18, 20, 22]      # Three Node.js versions
        # This creates 3 x 3 = 9 parallel jobs

      fail-fast: false                  # Continue other jobs if one fails
      max-parallel: 4                   # Limit concurrent jobs

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install and test
        run: |
          npm ci
          npm test
```

```yaml
# Matrix with include and exclude
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
        exclude:
          - os: windows-latest            # Skip Python 3.10 on Windows
            python-version: '3.10'
        include:
          - os: ubuntu-latest             # Add an extra combination
            python-version: '3.13'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt && pytest
```

---

## Caching

```yaml
# Cache dependencies to speed up workflows
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Explicit cache with actions/cache
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip             # Directory to cache
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: ${{ runner.os }}-pip-  # Fallback if no exact match
      - run: pip install -r requirements.txt

      # Many setup actions have built-in caching
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'                   # Automatically caches npm dependencies
```

---

## Artifacts

```yaml
# Upload and download build artifacts between jobs
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output             # Artifact name
          path: dist/                    # Path to upload
          retention-days: 7              # How long to keep (default 90)

  deploy:
    needs: build                         # Wait for build job to complete
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output             # Must match the upload name
          path: dist/
      - run: echo "Deploying build artifacts..."
```

---

## Conditional Execution

```yaml
# Use 'if' conditions to control when steps and jobs run
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'           # Only on main branch
        run: echo "Deploying to production..."
      - name: PR check
        if: github.event_name == 'pull_request'       # Only on PRs
        run: echo "This is a pull request"
      - name: Cleanup
        if: always()                                   # Runs regardless of status
        run: echo "Cleaning up..."
      - name: Notify on failure
        if: failure()                                  # Only if a step failed
        run: echo "Build failed!"

  # Conditional job execution
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: { name: production, url: 'https://myapp.com' }
    steps:
      - run: echo "Deploying..."
```

---

## Reusable Workflows

### Defining a Reusable Workflow

```yaml
# File: .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:                       # Makes this workflow callable
    inputs:
      node-version:
        description: 'Node.js version'
        required: false
        default: '20'
        type: string
    secrets:
      codecov-token:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Calling a Reusable Workflow

```yaml
# File: .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test-node-20:
    uses: ./.github/workflows/reusable-test.yml  # Call the reusable workflow
    with:
      node-version: '20'
    secrets:
      codecov-token: ${{ secrets.CODECOV_TOKEN }}

  test-node-18:
    uses: ./.github/workflows/reusable-test.yml  # Same workflow, different input
    with:
      node-version: '18'
```

---

## Common CI/CD Patterns

### Test, Lint, Build, Deploy Pipeline

```yaml
# File: .github/workflows/pipeline.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint              # Check code style and errors

  test:
    runs-on: ubuntu-latest
    needs: lint                        # Run after linting passes
    services:
      postgres:                        # Service container for testing
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
        run: npm test -- --coverage

  build:
    runs-on: ubuntu-latest
    needs: test                        # Run after tests pass
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with: { name: build, path: dist/ }

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: { name: production, url: 'https://myapp.example.com' }
    steps:
      - uses: actions/download-artifact@v4
        with: { name: build, path: dist/ }
      - name: Deploy to server
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: echo "Deploying..."       # Replace with actual deploy command
```

### Python CI Pattern

```yaml
name: Python CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: |
          pip install -r requirements.txt   # Install project deps
          pip install flake8 pytest          # Install dev tools
      - run: flake8 . --count --show-source --statistics  # Lint
      - run: pytest --verbose --tb=short                  # Test
```

---

## Docker Container Actions

```yaml
# Run the entire job inside a Docker container
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: node:20-alpine              # All steps run in this container
      env: { NODE_ENV: test }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
```

```yaml
# Build and push Docker images
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: user/app:latest,user/app:${{ github.sha }}
          cache-from: type=gha             # Use GitHub Actions cache
          cache-to: type=gha,mode=max
```

---

## Self-Hosted Runners

### Setting Up a Self-Hosted Runner

```bash
# Settings > Actions > Runners > New self-hosted runner
# Download, extract, and configure the runner package
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf actions-runner-linux-x64.tar.gz

# Configure and start (requires a registration token from GitHub)
./config.sh --url https://github.com/owner/repo --token YOUR_TOKEN
./run.sh                 # Run interactively
sudo ./svc.sh install    # Or install as a system service
sudo ./svc.sh start
```

```yaml
# Use a self-hosted runner in a workflow
jobs:
  build:
    runs-on: self-hosted           # Use any available self-hosted runner
    # runs-on: [self-hosted, linux, x64]  # Filter by labels
    steps:
      - uses: actions/checkout@v4
      - run: echo "Running on $(hostname)"
```

---

## Practice Exercises

### Exercise 1: Basic CI Workflow

```yaml
# Create .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci              # Install dependencies
      - run: npm run lint        # Run linter
      - run: npm test            # Run tests
```

### Exercise 2: Matrix Testing

```yaml
# Test across multiple Node.js versions and operating systems
name: Matrix Test
on: push

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

---

## Summary

GitHub Actions provides a powerful, integrated CI/CD platform with these key capabilities:

- **Workflow files**: YAML-based automation triggered by repository events
- **Actions marketplace**: Thousands of reusable actions for common tasks
- **Secrets management**: Encrypted storage for sensitive values
- **Matrix strategy**: Parallel testing across multiple configurations
- **Caching and artifacts**: Speed up builds and share data between jobs
- **Conditional execution**: Fine-grained control over when steps and jobs run
- **Reusable workflows**: DRY principles applied to CI/CD pipelines
- **Docker support**: Container-based jobs and image building

---

## Next Steps

- Build a complete CI/CD pipeline for your project
- Explore the GitHub Actions Marketplace for useful actions
- Set up deployment workflows with environment protection rules
- Learn about OpenID Connect (OIDC) for cloud provider authentication
- Create custom composite and Docker actions for your team

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [GitHub Actions Starter Workflows](https://github.com/actions/starter-workflows)
- [Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides)
