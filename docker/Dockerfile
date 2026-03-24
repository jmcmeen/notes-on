# Stage 1: Build the MkDocs static site
FROM python:3.12-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir \
    mkdocs-material==9.5.* \
    pymdown-extensions

COPY mkdocs.yml .
COPY docker/overrides/ docker/overrides/

# MkDocs expects docs_dir: docs, so assemble content there
RUN mkdir -p docs/notes
COPY README.md docs/
COPY notes/ docs/notes/

RUN mkdocs build --site-dir /build/site

# Stage 2: Runtime with nginx + download API
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    weasyprint \
    markdown

WORKDIR /app

# Copy built static site
COPY --from=builder /build/site /usr/share/nginx/html

# Copy notes for download API
COPY notes/ /app/notes/

# Copy application files from docker/ directory
COPY docker/download_api.py /app/
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Remove default nginx site
RUN rm -f /etc/nginx/sites-enabled/default

ENV NOTES_DIR=/app/notes

EXPOSE 80

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
