# Global ARG
ARG PYTHON_VERSION

# Build stage
FROM python:${PYTHON_VERSION}-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    binutils \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    make \
    g++ \
    zlib-dev \
    rust \
    cargo \
    openssl \
    openssl-dev \
    pkgconfig

# Set environment variables for OpenSSL
ENV OPENSSL_DIR=/usr \
    PKG_CONFIG_PATH=/usr/lib/pkgconfig

# Install Poetry and PyInstaller
RUN pip install --no-cache-dir poetry pyinstaller poethepoet

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY qbittorrent_add_trackers ./qbittorrent_add_trackers
COPY build_scripts ./build_scripts

# Install project dependencies
RUN poetry install --no-dev

# Build binary
RUN poe package

# Final stage
FROM alpine

# Set working directory
WORKDIR /app

# Copy binary from build stage
COPY --from=builder /app/dist/qbittorrent-add-trackers /app/qbittorrent-add-trackers
COPY config.base.yaml ./

# Set entrypoint
ENTRYPOINT ["./qbittorrent-add-trackers"]
