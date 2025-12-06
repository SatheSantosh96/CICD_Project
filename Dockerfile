# === Stage 1: Build Stage (Handles packaging/PyInstaller) ===
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies needed for Tkinter (tcl-dev/tk-dev for linking)
# and the SQLite3 system libraries for PyInstaller to link against.
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcl-dev tk-dev \
    sqlite3 \
    # Clean up to reduce image size
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install PyInstaller and Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir pyinstaller -r requirements.txt

# Copy application code
COPY . .

# Package the application into a single executable
RUN pyinstaller --onefile dashboard.py

# === Stage 2: Final Runtime Stage (Minimal environment) ===
FROM ubuntu:24.04

# Define variables for the graphical display environment
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0.0

# Install only the necessary runtime dependencies for the packaged GUI app to run.
# libx11-6, libxext6, libxtst6 are essential for X11/Tkinter.
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    python3 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libgtk-3-0 \
    libx11-6 \
    tcl tk \
    # Needed for image libraries like Pillow/PIL if used in the GUI
    libgdk-pixbuf-2.0-0 libjpeg-turbo8 libtiff6 libpng16-16 \
    # Clean up to reduce image size
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set application working directory and create a persistent data directory
WORKDIR /app
RUN mkdir -p /app/data

# Copy the packaged executable and the database script from the builder stage
COPY --from=builder /app/dist/dashboard ./
COPY create_db.py .

# Copy and set up the entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Declare a volume where the persistent SQLite file will live. 
# This is where the host machine must mount a local directory for persistence.
VOLUME /app/data

# The ENTRYPOINT runs the setup script, and the CMD provides the default executable
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["./dashboard"]