# Introduction to Docker

A comprehensive guide to Docker containerization, covering images, containers, Dockerfiles, Docker Compose, networking, volumes, and common deployment patterns.

---

## Table of Contents

- [What is Docker](#what-is-docker)
- [Installation](#installation)
- [Images](#images)
- [Containers](#containers)
- [Dockerfile](#dockerfile)
- [Docker Compose](#docker-compose)
- [Networking](#networking)
- [Volumes and Persistence](#volumes-and-persistence)
- [Docker Registry](#docker-registry)
- [Common Patterns](#common-patterns)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Docker

Docker is a platform for developing, shipping, and running applications inside lightweight, portable containers. Containers package an application with all its dependencies, ensuring consistent behavior across development, testing, and production environments.

### Containers vs Virtual Machines

| Aspect | Containers | Virtual Machines |
| ------ | ---------- | ---------------- |
| Isolation | Process-level (shared kernel) | Full OS isolation (hypervisor) |
| Size | Megabytes (10-500 MB) | Gigabytes (1-20 GB) |
| Startup | Seconds | Minutes |
| Density | Hundreds per host | Tens per host |

### Docker Architecture

- **Docker Engine/Daemon**: Runtime that builds, runs, and manages containers
- **Docker CLI**: Command-line interface for interacting with the daemon
- **Images**: Read-only templates; **Containers**: Running instances of images
- **Registry**: Storage and distribution service for images (e.g., Docker Hub)

---

## Installation

```bash
# Install Docker on Ubuntu/Debian
sudo apt update
sudo apt install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to the docker group (avoids needing sudo)
sudo usermod -aG docker $USER

# Verify the installation
docker --version        # Check Docker CLI version
docker run hello-world  # Pull and run a test container

# macOS: brew install --cask docker
```

---

## Images

### Pulling and Managing Images

```bash
# Pull images from Docker Hub
docker pull ubuntu:22.04       # Pull a specific tag
docker pull python:3.12-slim   # Slim Python image
docker pull node:20-alpine     # Alpine-based (smaller) image

# List and inspect images
docker images                  # Show all local images
docker history python:3.12     # Show image layer history

# Remove and clean up images
docker rmi ubuntu:22.04        # Remove a specific image
docker image prune -a          # Remove all unused images

# Tag an image
docker tag myapp:latest myapp:v1.0.0            # Add a version tag
docker tag myapp:latest registry.com/myapp:v1.0.0  # Tag for a registry

# Save and load images (for offline transfer)
docker save myapp:latest > myapp.tar            # Export to tarball
docker load < myapp.tar                          # Import from tarball
```

---

## Containers

### Running Containers

```bash
# Run a container from an image
docker run ubuntu:22.04 echo "Hello Docker"        # Run command and exit
docker run -it ubuntu:22.04 /bin/bash              # Interactive terminal
docker run -d nginx:latest                          # Detached (background)
docker run -d --name my-nginx nginx:latest          # With a custom name
docker run --rm ubuntu:22.04 echo "Temporary"       # Auto-remove on exit

# Port mapping
docker run -d -p 8080:80 nginx:latest              # Host:container port mapping
docker run -d -p 127.0.0.1:8080:80 nginx           # Bind to localhost only

# Volumes and environment
docker run -d -v /host/path:/container/path nginx  # Bind mount
docker run -d -v myvolume:/data nginx              # Named volume
docker run -d -e MYSQL_ROOT_PASSWORD=secret mysql:8 # Environment variable
docker run -d --env-file .env myapp:latest          # Load env from file

# Resource limits and restart policy
docker run -d --memory=512m --cpus=1.5 myapp:latest
docker run -d --restart unless-stopped nginx
```

### Managing Containers

```bash
# List containers
docker ps                      # Running containers
docker ps -a                   # All containers (including stopped)

# Lifecycle commands
docker start my-nginx          # Start a stopped container
docker stop my-nginx           # Graceful stop (SIGTERM then SIGKILL)
docker restart my-nginx        # Stop and start
docker rm my-nginx             # Remove a stopped container
docker rm -f my-nginx          # Force remove a running container

# Execute commands inside a running container
docker exec my-nginx ls /etc/nginx    # Run a command
docker exec -it my-nginx /bin/bash    # Open an interactive shell

# View logs
docker logs my-nginx           # Show all logs
docker logs -f my-nginx        # Follow log output (like tail -f)
docker logs --tail 50 my-nginx # Show last 50 lines

# Copy files and inspect
docker cp my-nginx:/etc/nginx/nginx.conf ./  # Container to host
docker cp ./index.html my-nginx:/usr/share/nginx/html/  # Host to container
docker inspect my-nginx        # Detailed JSON metadata
docker container prune         # Remove all stopped containers
```

---

## Dockerfile

### Basic Dockerfile Instructions

```dockerfile
# Dockerfile for a Python web application

# FROM: Specify the base image
FROM python:3.12-slim

# LABEL: Add metadata to the image
LABEL maintainer="developer@example.com"
LABEL description="Python web application"

# ENV: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN: Execute commands during the build process
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
# Combine RUN commands with && to reduce layers
# Clean up apt cache to keep image small

# WORKDIR: Set the working directory inside the container
WORKDIR /app

# COPY: Copy files from build context to image
COPY requirements.txt .
# Copy requirements first for better caching (layer won't rebuild unless file changes)

RUN pip install --no-cache-dir -r requirements.txt
# Install dependencies in a separate layer for caching

# COPY the application code (changes frequently, so copy last)
COPY . .

# EXPOSE: Document which port the app uses (informational only)
EXPOSE 8000

# CMD: Default command when container starts (can be overridden)
CMD ["python", "app.py"]
```

### ENTRYPOINT vs CMD

```dockerfile
# CMD: default command, fully overridden by docker run arguments
# ENTRYPOINT: fixed executable, CMD provides default arguments
# Common pattern:
FROM python:3.12-slim
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "app:app"]
# docker run myapp                             -> gunicorn with defaults
# docker run myapp --bind 0.0.0.0:5000 app:app -> overrides CMD args only
```

### Multi-Stage Builds

```dockerfile
# Multi-stage builds reduce final image size by separating build and runtime

# Stage 1: Build the application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci                           # Install all dependencies (including dev)
COPY . .
RUN npm run build                    # Generate production build

# Stage 2: Production image (only runtime dependencies)
FROM node:20-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production         # Install only production dependencies
COPY --from=builder /app/dist ./dist # Copy build output from builder stage
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

```dockerfile
# Multi-stage build for a Go application
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download                  # Download dependencies
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server .  # Static binary

# Final image: scratch (empty base) for minimal size
FROM scratch
COPY --from=builder /app/server /server   # Only the binary, nothing else
EXPOSE 8080
ENTRYPOINT ["/server"]
# Result: Image is just a few MB instead of hundreds
```

### .dockerignore

```dockerfile
# File: .dockerignore - prevents files from being included in the build context
.git
node_modules
venv
__pycache__
dist
.vscode
.idea
Dockerfile
docker-compose.yml
.env
*.pem
README.md
tests/
```

### Dockerfile Best Practices

```dockerfile
# 1. Use specific tags: FROM python:3.12-slim (not "latest")
# 2. Use slim/alpine variants: FROM node:20-alpine (~50MB vs ~350MB)
# 3. Use a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app appuser
USER appuser
# 4. Order: least-changing first (base, deps, code)
# 5. Combine RUN commands to reduce layers and clean up
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
# 6. Use COPY instead of ADD (unless you need tar extraction)
# 7. Use health checks
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### Building Images

```bash
docker build -t myapp:latest .                          # Build from current dir
docker build -f Dockerfile.prod -t myapp:prod .         # Specific Dockerfile
docker build --build-arg APP_VERSION=2.0.0 -t myapp .   # With build args
docker build --no-cache -t myapp:latest .                # Force rebuild
docker build --target builder -t myapp:builder .         # Multi-stage target
```

---

## Docker Compose

### Basic docker-compose.yml

```yaml
# File: docker-compose.yml (or compose.yml for v2)

# Services define the containers to run
services:
  web:
    build: .                          # Build from Dockerfile in current dir
    ports:
      - "8080:8000"                   # Map host port 8080 to container port 8000
    environment:
      - DATABASE_URL=postgres://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db                            # Start db before web
      - cache                         # Start cache before web
    volumes:
      - .:/app                        # Bind mount for development (live reload)
    restart: unless-stopped

  db:
    image: postgres:16-alpine         # Use a pre-built image
    environment:
      POSTGRES_DB: mydb               # Database name
      POSTGRES_USER: postgres         # Database user
      POSTGRES_PASSWORD: secret       # Database password (use secrets in prod)
    volumes:
      - postgres-data:/var/lib/postgresql/data  # Persist database data
    ports:
      - "5432:5432"                   # Expose for local development tools

  cache:
    image: redis:7-alpine             # Redis cache service
    ports:
      - "6379:6379"

# Named volumes for data persistence
volumes:
  postgres-data:                      # Docker manages this volume
```

### Docker Compose Commands

```bash
# Start and stop services
docker compose up                   # Run in foreground (shows logs)
docker compose up -d                # Detached mode (background)
docker compose up --build           # Rebuild images before starting
docker compose down                 # Stop and remove containers, networks
docker compose down -v              # Also remove volumes (destroys data)

# Monitoring and interaction
docker compose ps                   # List service containers
docker compose logs -f web          # Follow logs for a service
docker compose exec web bash        # Shell into a running service
docker compose run --rm web python manage.py migrate  # One-off command

# Scaling and building
docker compose up -d --scale web=3  # Run multiple instances
docker compose build                # Build all service images
```

### Advanced Compose Features

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
      target: production              # Multi-stage build target
    ports: ["8080:8000"]
    networks: [frontend, backend]
    env_file: [.env]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      db:
        condition: service_healthy    # Wait for health check to pass

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}  # Env var with default
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s

networks:
  frontend:
    driver: bridge
  backend:
    internal: true                    # No external access

volumes:
  postgres-data:
```

---

## Networking

### Network Types and Communication

```bash
# Default networks: bridge (isolated), host (shared), none
docker network ls                    # Show all networks

# Create and use a custom bridge network
docker network create app-network
docker run -d --name web --network app-network nginx
docker run -d --name api --network app-network node-app
# Containers on custom networks can communicate by name: http://api:3000

# Connect/disconnect running containers
docker network connect app-network existing-container
docker network disconnect app-network existing-container

# Host network (Linux only): container uses host's network directly
docker run -d --network host nginx   # No port mapping needed

# Inter-container communication example
docker network create backend
docker run -d --name postgres --network backend \
  -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name app --network backend \
  -e DATABASE_URL=postgres://postgres:secret@postgres:5432/mydb myapp:latest

# Cleanup
docker network rm app-network       # Remove a network
docker network prune                # Remove all unused networks
```

---

## Volumes and Persistence

```bash
# Volumes provide persistent storage (data survives container removal)
docker volume create mydata
docker volume ls                    # List volumes

# Mount types
docker run -d -v mydata:/app/data myapp              # Named volume
docker run -d -v $(pwd):/app myapp                   # Bind mount (host dir)
docker run -d -v $(pwd)/config:/app/config:ro myapp  # Read-only mount
docker run -d --tmpfs /app/temp myapp                # In-memory tmpfs

# Cleanup
docker volume rm mydata             # Remove a specific volume
docker volume prune                 # Remove all unused volumes

# Backup and restore a volume
docker run --rm -v mydata:/source -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /source .
docker run --rm -v mydata:/target -v $(pwd):/backup alpine \
  tar xzf /backup/backup.tar.gz -C /target
```

---

## Docker Registry

```bash
# Push to Docker Hub
docker login
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# Use a private registry
docker login registry.example.com
docker tag myapp:latest registry.example.com/myapp:latest
docker push registry.example.com/myapp:latest

# Run a local registry for development
docker run -d -p 5000:5000 --name registry registry:2
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest
```

---

## Common Patterns

### Python Application

```dockerfile
# Dockerfile for a Python Flask/FastAPI application
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

```yaml
# docker-compose.yml for Python app with database
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app                       # Mount source for development

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### Node.js Application

```dockerfile
# Dockerfile for a Node.js application
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Install dependencies (cached layer)
COPY package*.json ./
RUN npm ci --only=production  # Install only production dependencies

# Copy application source
COPY . .

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml for Node.js with MongoDB and Redis
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MONGODB_URI=mongodb://mongo:27017/myapp
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=production
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:7                    # MongoDB database
    volumes:
      - mongo-data:/data/db          # Persist database
    ports:
      - "27017:27017"

  redis:
    image: redis:7-alpine            # Redis cache
    volumes:
      - redis-data:/data             # Persist Redis data
    ports:
      - "6379:6379"

volumes:
  mongo-data:
  redis-data:
```

### Database Containers

```bash
# PostgreSQL
docker run -d --name postgres -e POSTGRES_DB=mydb -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:16-alpine
docker exec -it postgres psql -U postgres -d mydb  # Connect

# MySQL
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=mydb \
  -v mysqldata:/var/lib/mysql -p 3306:3306 mysql:8
docker exec -it mysql mysql -u root -p mydb  # Connect

# MongoDB
docker run -d --name mongo -v mongodata:/data/db -p 27017:27017 mongo:7
docker exec -it mongo mongosh  # Connect

# Redis
docker run -d --name redis -v redisdata:/data -p 6379:6379 redis:7-alpine
docker exec -it redis redis-cli  # Connect
```

---

## Practice Exercises

### Exercise 1: Build and Run a Simple Container

```bash
# 1. Create a project with a simple Python app and Dockerfile
mkdir docker-practice && cd docker-practice
echo 'from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
class H(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message":"Hello Docker!"}).encode())
HTTPServer(("0.0.0.0",8000),H).serve_forever()' > app.py

echo 'FROM python:3.12-slim
WORKDIR /app
COPY app.py .
EXPOSE 8000
CMD ["python","app.py"]' > Dockerfile

# 2. Build, run, test, and clean up
docker build -t practice-app .
docker run -d -p 8080:8000 --name practice practice-app
curl http://localhost:8080
docker stop practice && docker rm practice
```

### Exercise 2: Docker Compose Multi-Service Application

```yaml
# Create a docker-compose.yml with a web app and database
# File: docker-compose.yml

services:
  web:
    build: .
    ports:
      - "8080:8000"
    depends_on:
      - db
    environment:
      - DB_HOST=db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: practice
      POSTGRES_DB: practicedb
    volumes:
      - practice-data:/var/lib/postgresql/data

volumes:
  practice-data:
```

```bash
# Start the services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs

# Access the database
docker compose exec db psql -U postgres -d practicedb

# Stop and clean up
docker compose down -v
```

### Exercise 3: Multi-Stage Build

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (much smaller image)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

### Exercise 4: Custom Network Communication

```bash
# Create a network and test container-to-container communication
docker network create exercise-net
docker run -d --name backend --network exercise-net nginx
docker run -d --name frontend --network exercise-net alpine sleep 3600
docker exec frontend ping -c 3 backend  # Resolves by container name

# Clean up
docker stop backend frontend && docker rm backend frontend
docker network rm exercise-net
```

---

## Summary

Docker provides a powerful containerization platform for modern application development and deployment:

- **Images**: Immutable templates built from Dockerfiles, pulled from registries
- **Containers**: Lightweight, isolated runtime instances of images
- **Dockerfile**: Declarative instructions for building reproducible images
- **Multi-stage builds**: Separate build and runtime for smaller production images
- **Docker Compose**: Multi-container application orchestration with YAML
- **Networking**: Bridge, host, and custom networks for container communication
- **Volumes**: Persistent data storage that survives container lifecycle
- **Registry**: Image distribution via Docker Hub or private registries
- **Best practices**: Non-root users, slim images, layer caching, health checks

---

## Next Steps

- Learn Kubernetes for container orchestration at scale
- Study container security best practices and image scanning
- Learn about Docker BuildKit for advanced build features
- Explore Podman as a daemonless alternative to Docker
- Study container monitoring with Prometheus and Grafana

---

## Additional Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Play with Docker (interactive lab)](https://labs.play-with-docker.com/)
