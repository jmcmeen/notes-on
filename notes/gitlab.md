# Introduction to GitLab

A comprehensive guide to GitLab, the complete DevOps platform providing Git repository management, CI/CD, issue tracking, and more in a single application.

---

## Table of Contents

- [What is GitLab](#what-is-gitlab)
- [Repository Management](#repository-management)
- [Merge Requests](#merge-requests)
- [CI/CD](#cicd)
- [GitLab Container Registry](#gitlab-container-registry)
- [GitLab Pages](#gitlab-pages)
- [Issue Tracking and Boards](#issue-tracking-and-boards)
- [Wiki](#wiki)
- [Variables and Secrets](#variables-and-secrets)
- [Environments and Deployments](#environments-and-deployments)
- [Auto DevOps](#auto-devops)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is GitLab

GitLab is an open-source DevOps platform providing a complete set of tools for the software development lifecycle. Unlike GitHub, which started as a code hosting platform, GitLab was built as an integrated DevOps solution.

### GitLab vs GitHub

| Feature | GitLab | GitHub |
| ------- | ------ | ------ |
| Hosting | Self-hosted or SaaS (gitlab.com) | SaaS (github.com) or Enterprise Server |
| CI/CD | Built-in (.gitlab-ci.yml) | GitHub Actions (.github/workflows/) |
| Code Review | Merge Requests | Pull Requests |
| Container Registry | Built-in | GitHub Packages |
| Issue Boards | Built-in Kanban | GitHub Projects |
| Wiki | Built-in per project | Built-in per repo |
| Self-Hosting | Free Community Edition | Enterprise only (paid) |
| DevOps Scope | Full DevOps platform | Primarily code + CI/CD |

GitLab is available in Free, Premium, and Ultimate tiers, ranging from core features to full DevSecOps with security scanning and compliance.

---

## Repository Management

### Creating and Cloning Repositories

```bash
# Clone a repository from GitLab
git clone https://gitlab.com/username/project.git    # HTTPS
git clone git@gitlab.com:username/project.git        # SSH

# Clone a specific branch
git clone -b develop https://gitlab.com/username/project.git

# Add GitLab as a remote to an existing project
cd existing-project
git remote add origin https://gitlab.com/username/project.git
git push -u origin main  # Push and set upstream tracking
```

### Repository Settings and Forking

```bash
# GitLab repositories are organized into namespaces:
# - Personal: gitlab.com/username/project
# - Group: gitlab.com/group/subgroup/project
# Visibility options: Private, Internal (logged-in users), or Public

# Push an existing repository to GitLab
cd existing-project
git remote add origin https://gitlab.com/username/project.git
git push --all origin && git push --tags origin

# Fork workflow: Fork via web UI, then clone and add upstream
git clone git@gitlab.com:your-username/forked-project.git
cd forked-project
git remote add upstream git@gitlab.com:original-owner/project.git
git fetch upstream && git merge upstream/main  # Sync with upstream
```

---

## Merge Requests

### Creating Merge Requests

```bash
# Create a feature branch and push it
git checkout -b feature/user-auth
# ... make changes ...
git add .
git commit -m "Add user authentication"
git push -u origin feature/user-auth

# GitLab displays a "Create merge request" link after pushing
# You can also create MRs from the web UI:
# 1. Navigate to Merge Requests > New merge request
# 2. Select source branch (feature/user-auth) and target branch (main)
# 3. Fill in title, description, assignee, reviewers, labels

# Create MR from the command line using push options
git push -o merge_request.create \
  -o merge_request.target=main \
  -o merge_request.title="Add user authentication" \
  -o merge_request.description="Implements login and signup endpoints" \
  -o merge_request.assign="username" \
  -o merge_request.label="feature" \
  origin feature/user-auth

# Remove source branch after merge
git push -o merge_request.create \
  -o merge_request.remove_source_branch \
  origin feature/user-auth
```

### Reviewing and Approvals

```bash
# Review workflow: Changes tab > inline comments > threads > Approve/Request changes

# Checkout a merge request locally for testing
git fetch origin merge-requests/42/head:mr-42  # Fetch MR #42
git checkout mr-42                              # Switch to the MR branch

# Approval rules (Premium tier): set in Settings > Merge requests
# CODEOWNERS file (.gitlab/CODEOWNERS) for automatic reviewers:
# * @default-approver
# *.py @python-team
# /docs/ @docs-team
```

---

## CI/CD

### Basic .gitlab-ci.yml

```yaml
# File: .gitlab-ci.yml (placed in the repository root)

# Define the stages of the pipeline (order matters)
stages:
  - build
  - test
  - deploy

# Default settings applied to all jobs
default:
  image: node:20-alpine    # Docker image for all jobs unless overridden

# Global variables available to all jobs
variables:
  NODE_ENV: test           # Set environment variable for all jobs

# Build stage
build:
  stage: build
  script:
    - npm ci               # Install dependencies from lockfile
    - npm run build        # Create production build
  artifacts:
    paths:
      - dist/              # Save build output for later stages
    expire_in: 1 hour      # Artifact retention period

# Test stage
test:
  stage: test
  script:
    - npm ci
    - npm run lint         # Run linter
    - npm test             # Run test suite
  coverage: '/Statements\s*:\s*(\d+\.?\d*)%/'  # Extract coverage from output

# Deploy stage (only on main branch)
deploy:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - npm run deploy       # Run deployment script
  only:
    - main                 # Only run on the main branch
  when: manual             # Require manual trigger in the UI
```

### Jobs and Stages

```yaml
# Jobs run in parallel within the same stage
# Jobs in the next stage wait for the previous stage to complete

stages:
  - prepare
  - test
  - package
  - deploy

install-deps:
  stage: prepare
  script:
    - npm ci
  artifacts:
    paths:
      - node_modules/      # Pass installed deps to subsequent jobs
    expire_in: 30 minutes

unit-tests:
  stage: test
  needs: [install-deps]    # Explicit dependency (DAG mode)
  script:
    - npm run test:unit

integration-tests:
  stage: test
  needs: [install-deps]    # Both test jobs run in parallel
  services:
    - postgres:16-alpine   # Service container (accessible as "postgres" hostname)
  variables:
    POSTGRES_DB: testdb
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgres://postgres:testpass@postgres:5432/testdb
  script:
    - npm run test:integration

build-image:
  stage: package
  image: docker:24                 # Use Docker-in-Docker image
  services:
    - docker:24-dind               # Docker daemon as a service
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA
```

### Runners

```bash
# Runner types: Shared (all projects), Group, or Project-specific

# Install and register a GitLab Runner
sudo curl -L --output /usr/local/bin/gitlab-runner \
  https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
sudo chmod +x /usr/local/bin/gitlab-runner
sudo gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token YOUR_TOKEN \
  --executor docker \
  --docker-image alpine:latest
sudo gitlab-runner start
```

### Artifacts and Caching

```yaml
# Artifacts: Pass files between jobs in a pipeline
build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/                   # Files to save
    reports:
      junit: test-results.xml   # Special report types for GitLab UI
    expire_in: 1 week
    when: always                # Save artifacts even on failure

# Caching: Reuse files across pipeline runs
test:
  stage: test
  cache:
    key: $CI_COMMIT_REF_SLUG           # Cache per branch
    paths:
      - node_modules/
    fallback_keys:
      - npm-main                       # Fall back to main branch cache
  script:
    - npm ci
    - npm test
```

---

## GitLab Container Registry

```bash
# Built-in Docker registry per project
docker login registry.gitlab.com
docker build -t registry.gitlab.com/username/project:latest .
docker push registry.gitlab.com/username/project:latest
docker pull registry.gitlab.com/username/project:latest
```

```yaml
# Build and push in CI/CD
build-docker:
  stage: package
  image: docker:24
  services:
    - docker:24-dind
  variables:
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA   # Auto-set by GitLab
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .     # Build the image
    - docker push $IMAGE_TAG           # Push to GitLab registry
    - docker tag $IMAGE_TAG $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
```

---

## GitLab Pages

```yaml
# GitLab Pages hosts static websites from your repository
# The job must be named "pages" and output to the "public" directory

# Static site deployment
pages:
  stage: deploy
  script:
    - mkdir -p public                  # Create the output directory
    - cp -r dist/* public/             # Copy build output to public
  artifacts:
    paths:
      - public                         # GitLab serves files from this directory
  only:
    - main                             # Deploy only from main branch

# Hugo site example
pages:
  image: registry.gitlab.com/pages/hugo:latest
  script:
    - hugo                             # Hugo outputs to public/ by default
  artifacts:
    paths:
      - public
  only:
    - main

# Your site will be at: https://username.gitlab.io/project-name/
# For user/group pages: https://username.gitlab.io/ (project must be named username.gitlab.io)
```

---

## Issue Tracking and Boards

```bash
# GitLab provides built-in issue tracking with:
# Labels, Milestones, Weights, Due dates, Assignees, Related issues
# Scoped labels use "::" (e.g., priority::high) - only one per scope

# Issue boards provide Kanban-style project management
# Default board: "Open" and "Closed" lists; add custom lists per label

# Close issues from commits: "Closes #15" or "Fixes #15, #16"

# Create issues via API
curl --request POST "https://gitlab.com/api/v4/projects/PROJECT_ID/issues" \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --data "title=Fix login bug&labels=bug&assignee_ids[]=12345"
```

---

## Wiki

```bash
# Each project has a built-in wiki (also a separate Git repository)
git clone git@gitlab.com:username/project.wiki.git
cd project.wiki

# Wiki pages are Markdown files; edit and push like any repo
echo "# Home Page" > home.md
git add . && git commit -m "Update wiki" && git push origin main
# Also editable via the GitLab web UI: Project > Wiki
```

---

## Variables and Secrets

```yaml
# Variables can be set at Instance, Group, Project, or Pipeline level
# Predefined variables: $CI_COMMIT_SHA, $CI_COMMIT_REF_NAME,
#   $CI_PIPELINE_ID, $CI_PROJECT_NAME, $CI_REGISTRY_IMAGE

variables:
  APP_VERSION: "1.0.0"              # Pipeline-level variable

deploy:
  stage: deploy
  script:
    - echo "Deploying version $APP_VERSION"
    - echo "Commit: $CI_COMMIT_SHORT_SHA"           # Predefined variable
  variables:
    DEPLOY_ENV: production                          # Job-level variable

# Protected variables: only available in protected branches/tags
# Masked variables: hidden in job logs
```

```bash
# Set variables via the API
curl --request POST "https://gitlab.com/api/v4/projects/PROJECT_ID/variables" \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --form "key=API_KEY" --form "value=secret-value" \
  --form "protected=true" --form "masked=true"
```

---

## Environments and Deployments

```yaml
deploy-staging:
  stage: deploy
  script:
    - echo "Deploying to staging..."
    - ./deploy.sh staging
  environment:
    name: staging                           # Environment name
    url: https://staging.example.com        # Environment URL (shown in GitLab UI)
  only:
    - develop

deploy-production:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  when: manual                              # Require manual approval
  only:
    - main

# Dynamic environments (per-branch review apps)
deploy-review:
  stage: deploy
  script:
    - ./deploy-review.sh $CI_COMMIT_REF_SLUG
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
  only: [merge_requests]

stop-review:
  stage: deploy
  script: [./teardown-review.sh $CI_COMMIT_REF_SLUG]
  environment: { name: "review/$CI_COMMIT_REF_SLUG", action: stop }
  when: manual
  only: [merge_requests]
```

---

## Auto DevOps

```yaml
# Auto DevOps provides zero-config CI/CD (Settings > CI/CD > Auto DevOps)
# Automatically runs: Build, Test, Code Quality, SAST, Dependency Scanning,
# Container Scanning, Review Apps, and Deploy to Kubernetes

# Customize by including the template and overriding variables:
include:
  - template: Auto-DevOps.gitlab-ci.yml

variables:
  AUTO_DEVOPS_PLATFORM_TARGET: ECS         # Deploy to AWS ECS instead of K8s
  POSTGRES_ENABLED: "false"                # Disable auto database provisioning
  TEST_DISABLED: "true"                    # Skip the test stage
```

---

## Practice Exercises

### Exercise 1: Basic CI/CD Pipeline

```yaml
# Three-stage pipeline with caching
stages: [build, test, deploy]
default:
  image: node:20-alpine

cache:
  key: $CI_COMMIT_REF_SLUG
  paths: [node_modules/]

build:
  stage: build
  script: [npm ci, npm run build]

test:
  stage: test
  script: [npm ci, npm test]

deploy:
  stage: deploy
  script: [echo "Deploying..."]
  only: [main]
  when: manual
```

### Exercise 2: Multi-Environment Deployment

```yaml
stages: [test, deploy]

test:
  stage: test
  image: python:3.12
  script: [pip install -r requirements.txt, pytest]

deploy-staging:
  stage: deploy
  script: [echo "Deploying to staging"]
  environment: { name: staging, url: 'https://staging.example.com' }
  only: [develop]

deploy-production:
  stage: deploy
  script: [echo "Deploying to production"]
  environment: { name: production, url: 'https://example.com' }
  only: [main]
  when: manual
```

### Exercise 3: Docker Build Pipeline

```yaml
# Build and push a Docker image to GitLab Container Registry
stages: [build, publish]

build-image:
  stage: build
  image: docker:24
  services: [docker:24-dind]
  variables: { DOCKER_TLS_CERTDIR: "/certs" }
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

publish-latest:
  stage: publish
  image: docker:24
  services: [docker:24-dind]
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  only: [main]
```

---

## Summary

GitLab provides a comprehensive DevOps platform with these essential capabilities:

- **Repository management**: Git hosting with groups, forks, and protected branches
- **Merge requests**: Code review with approvals and inline comments
- **CI/CD pipelines**: YAML-based pipeline configuration with stages and jobs
- **Container registry**: Built-in Docker image hosting per project
- **Issue tracking**: Full-featured issue management with boards and milestones
- **Environments**: Deploy tracking with staging, production, and review apps
- **Auto DevOps**: Zero-configuration CI/CD with automatic detection

---

## Next Steps

- Set up GitLab CI/CD for your existing projects
- Explore GitLab Security features (SAST, DAST, dependency scanning)
- Configure Kubernetes integration for container deployments
- Learn about GitLab Terraform integration for infrastructure as code
- Configure GitLab mirroring to sync with GitHub or other remotes

---

## Additional Resources

- [GitLab Documentation](https://docs.gitlab.com/)
- [GitLab CI/CD Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab University](https://university.gitlab.com/)
- [GitLab Forum](https://forum.gitlab.com/)
