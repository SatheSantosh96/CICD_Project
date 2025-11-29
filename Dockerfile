# === Stage 1: Build Stage (Handles packaging/PyInstaller) ===
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies needed for Tkinter (tcl-dev/tk-dev for linking)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcl-dev tk-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install PyInstaller and Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir pyinstaller -r requirements.txt

# Copy application code
COPY . .

# Package the application into a single executable (PyInstaller)
# The final executable is named 'dashboard' (based on the main file)
RUN pyinstaller --onefile dashboard.py

# === Stage 2: Final Runtime Stage (Minimal environment) ===
FROM ubuntu:24.04

# Install only the necessary runtime dependencies for the packaged GUI app to run.
# These include essential X11 libraries (which Tkinter uses) and the DB.
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libgtk-3-0 \
    mesa-utils \
    tcl tk \
    # Needed for image libraries like Pillow/PIL if used in the GUI
    libgdk-pixbuf-2.0-0 libjpeg-turbo8 libtiff6 libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the packaged executable and the database script from the builder stage
COPY --from=builder /app/dist/dashboard ./
COPY create_db.py .

# The CMD needs to run the create_db script and then launch the app.
# We launch the executable, and since this is a GUI app, we must use a workaround
# for the display, typically by relying on X11 forwarding or VNC setup on the host.
CMD ["/bin/bash", "-c", "python create_db.py && ./dashboard"]