# ===============================
# RecordSync – Windows EXE Builder
# ===============================

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64

# -------------------------------
# 1. Install system dependencies
# -------------------------------
RUN dpkg --add-architecture i386 \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    cabextract \
    p7zip-full \
    unzip \
    wine64 \
    wine32 \
    winbind \
    xvfb \
    fonts-wine \
    python3 \
    python3-pip \
    dos2unix \
 && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 2. Working directory
# -------------------------------
WORKDIR /src
COPY . .

# -------------------------------
# 3. Install Windows Python
# -------------------------------
ENV PY_VER=3.11.7
ENV PY_EXE=python-3.11.7-amd64.exe

RUN set -eux; \
    wineboot --init; \
    wget -q https://www.python.org/ftp/python/${PY_VER}/${PY_EXE} -O /tmp/${PY_EXE}; \
    wine /tmp/${PY_EXE} /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1; \
    rm -f /tmp/${PY_EXE}; \
    sleep 5

# -------------------------------
# 4. Wine Python helper
# -------------------------------
RUN set -eux; \
    PYTHON_WIN=$(find /root/.wine/drive_c -iname python.exe | head -n 1); \
    if [ -z "$PYTHON_WIN" ]; then echo "❌ Python not found"; exit 1; fi; \
    echo '#!/bin/bash' > /usr/local/bin/wine-python; \
    echo "exec wine \"$PYTHON_WIN\" \"\$@\"" >> /usr/local/bin/wine-python; \
    chmod +x /usr/local/bin/wine-python; \
    wine-python -V

# -------------------------------
# 5. Install PyInstaller + deps
# -------------------------------
RUN set -eux; \
    wine-python -m pip install --upgrade pip setuptools wheel; \
    if [ -f requirements.txt ]; then \
        wine-python -m pip install -r requirements.txt; \
    fi; \
    wine-python -m pip install pyinstaller

# -------------------------------
# 6. Build recordsync.exe
# -------------------------------
RUN set -eux; \
    mkdir -p dist build; \
    wine-python -m PyInstaller \
        --onefile \
        --noconsole \
        --name recordsync \
        --distpath dist \
        --workpath build \
        --specpath build \
        main.py

# -------------------------------
# 7. Output volume
# -------------------------------
VOLUME ["/src/dist"]
CMD ["bash", "-lc", "echo 'Build complete'; ls -lh dist"]
