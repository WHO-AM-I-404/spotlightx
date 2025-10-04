# Running SpotlightX from Source

Complete guide to run SpotlightX directly from source code without building packages.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Running the Application](#running-the-application)
5. [Development Mode](#development-mode)
6. [Testing & Debugging](#testing--debugging)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

**For the impatient** - 3 commands to get started:

```bash
# 1. Clone & navigate
git clone https://github.com/WHO-AM-I-404/spotlightx && cd spotlightx

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run!
cd spotlightx && python run.py
```

Done! The application window should appear.

---

## Prerequisites

### System Requirements

- **Operating System**: Linux (Debian-based recommended)
  - Ubuntu 20.04+
  - Debian 11+
  - Linux Mint 20+
  - Pop!_OS 20.04+
  - Any Debian derivative

- **Python**: 3.11 or higher
- **RAM**: 2 GB minimum (4 GB recommended)
- **Disk Space**: 500 MB for dependencies

### Check Your Python Version

```bash
python3 --version
# Should show: Python 3.11.x or higher
```

If you don't have Python 3.11+:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Fedora
sudo dnf install python3.11

# Arch Linux
sudo pacman -S python311
```

### System Dependencies

Install required system packages:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    python3-tk \
    xdg-utils \
    libmagic1 \
    libxcb-cursor0 \
    libxkbcommon-x11-0

# Fedora
sudo dnf install python3-tkinter xdg-utils file-libs

# Arch Linux
sudo pacman -S tk xdg-utils file
```

---

## Installation Steps

### Method 1: Using pip (Recommended)

```bash
# Step 1: Clone repository
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx

# Step 2: Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# Step 3: Install Python dependencies
pip install -r requirements.txt

# Step 4: Verify installation
python -c "import PySide6, rapidfuzz; print('Dependencies OK!')"
```

### Method 2: Using uv (Faster)

```bash
# Install uv if not already installed
pip install uv

# Clone repository
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx

# Install dependencies (uv is much faster)
uv pip install -r requirements.txt

# Verify
python -c "import PySide6, rapidfuzz; print('Dependencies OK!')"
```

### Method 3: System-wide Installation

**Warning**: This installs packages globally. Use virtual environment instead.

```bash
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx
sudo pip3 install -r requirements.txt
```

---

## Running the Application

### Basic Run

Navigate to the `spotlightx` subdirectory and run:

```bash
cd spotlightx
python run.py
```

OR from project root:

```bash
python spotlightx/run.py
```

### Run with Logging

See detailed output:

```bash
cd spotlightx
python run.py 2>&1 | tee spotlightx.log
```

### Run in Background

```bash
cd spotlightx
nohup python run.py > /dev/null 2>&1 &
```

To stop:
```bash
pkill -f "python run.py"
# or
pkill -f spotlightx
```

### Run with Virtual Environment

If using venv:

```bash
# Activate venv
source venv/bin/activate

# Run
cd spotlightx
python run.py

# When done
deactivate
```

---

## Development Mode

### Interactive Development

For developing features:

```bash
# 1. Install in editable mode
pip install -e .

# 2. Run with auto-reload (manual restart for now)
cd spotlightx
python run.py
```

### Testing Individual Components

#### Test Indexer

```python
cd spotlightx
python3 << 'EOF'
from spotlightx.indexer import Indexer

# Create indexer
indexer = Indexer()

# Index applications
indexer.index_all()

# Check results
print(f"Found {len(indexer.get_apps())} applications")
print(f"Found {len(indexer.get_files())} files")

# Show first 5 apps
for app in indexer.get_apps()[:5]:
    print(f"  - {app['name']}")
EOF
```

#### Test Search Engine

```python
cd spotlightx
python3 << 'EOF'
from spotlightx.indexer import Indexer
from spotlightx.search import SearchEngine

# Initialize
indexer = Indexer()
indexer.index_all()

search_engine = SearchEngine(indexer)

# Search
results = search_engine.search('firefox')
print(f"Found {len(results)} results for 'firefox'")

for result in results[:3]:
    print(f"  - {result['name']}: {result['score']}")
EOF
```

#### Test Plugin System

```python
cd spotlightx
python3 << 'EOF'
from spotlightx.plugin_manager import PluginManager

# Create plugin manager
pm = PluginManager()

# Load plugins
pm.load_all_plugins()

# Test hook
results = pm.trigger_hook('on_query', 'test query')
print(f"Plugin responses: {results}")
EOF
```

### Development with Hot Reload

For rapid development, use a file watcher:

```bash
# Install watchdog
pip install watchdog

# Create watch script
cat > watch.sh << 'EOF'
#!/bin/bash
while inotifywait -e modify -r spotlightx/; do
    pkill -f "python run.py"
    cd spotlightx && python run.py &
done
EOF

chmod +x watch.sh
./watch.sh
```

---

## Testing & Debugging

### Manual Testing Checklist

1. **Application Launch**
   ```bash
   cd spotlightx && python run.py
   # ✓ Window appears
   # ✓ No errors in console
   ```

2. **Search Applications**
   ```
   Type: firefox
   # ✓ Firefox appears in results
   # ✓ Enter opens Firefox
   ```

3. **Search Files**
   ```
   Type: .pdf
   # ✓ PDF files listed
   # ✓ Shows file size and type
   ```

4. **Calculator**
   ```
   Type: 2 + 2
   # ✓ Shows result: 4
   # ✓ Result copied to clipboard
   ```

5. **Web Search**
   ```
   Type: g python tutorial
   # ✓ Shows "Search Google"
   # ✓ Opens browser with search
   ```

### Debug Mode

Run with debug output:

```bash
cd spotlightx
python run.py --verbose  # if implemented

# Or use Python logging
PYTHONPATH=. python -u run.py
```

### Check Cache Files

```bash
# View cached apps
cat ~/.cache/spotlightx/apps.json | jq '.[:3]'

# View cached files
cat ~/.cache/spotlightx/files.json | jq '.[:3]'

# View usage statistics
cat ~/.cache/spotlightx/usage.json | jq
```

### Performance Profiling

```bash
cd spotlightx
python3 << 'EOF'
import time
from spotlightx.indexer import Indexer

indexer = Indexer()

# Time indexing
start = time.time()
indexer.index_all()
elapsed = time.time() - start

print(f"Indexing took: {elapsed:.2f} seconds")
print(f"Apps: {len(indexer.get_apps())}")
print(f"Files: {len(indexer.get_files())}")
EOF
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'PySide6'

**Solution**:
```bash
pip install PySide6
# or
pip install -r requirements.txt
```

#### 2. ModuleNotFoundError: No module named 'spotlightx'

**Solution**:
```bash
# Make sure you're in the right directory
cd spotlightx  # the subdirectory
python run.py

# OR run from project root
python spotlightx/run.py
```

#### 3. Tkinter not found

**Solution**:
```bash
sudo apt install python3-tk
```

#### 4. No applications found

**Solution**:
```bash
# Check .desktop file locations
ls /usr/share/applications/
ls ~/.local/share/applications/

# Force re-index
rm ~/.cache/spotlightx/apps.json
cd spotlightx && python run.py
```

#### 5. Window doesn't appear

**Solution**:
```bash
# Check if process is running
ps aux | grep python.*spotlightx

# Check for errors
cd spotlightx
python run.py 2>&1 | grep -i error

# Try with display explicitly set
DISPLAY=:0 python run.py
```

#### 6. Permission denied errors

**Solution**:
```bash
# Fix cache directory permissions
chmod 755 ~/.cache/spotlightx/
chmod 644 ~/.cache/spotlightx/*.json

# Fix config directory
chmod 755 ~/.config/spotlightx/
```

#### 7. High memory usage

**Solution**:
```bash
# Reduce indexed files
# Edit indexer.py or create config
nano ~/.config/spotlightx/config.json

# Add:
{
  "max_files": 5000,
  "file_roots": [
    "~/Documents",
    "~/Downloads"
  ]
}
```

### Getting Help

If issues persist:

1. **Check logs**:
   ```bash
   cd spotlightx
   python run.py 2>&1 | tee debug.log
   # Share debug.log
   ```

2. **System info**:
   ```bash
   python3 --version
   pip list | grep -E "(PySide6|rapidfuzz|watchdog)"
   uname -a
   echo $DISPLAY
   ```

3. **Report issue**: https://github.com/WHO-AM-I-404/spotlightx/issues

---

## Advanced Usage

### Custom Configuration

Create `~/.config/spotlightx/config.json`:

```json
{
  "max_results": 15,
  "file_roots": [
    "~/Documents",
    "~/Projects",
    "~/Downloads"
  ],
  "desktop_paths": [
    "/usr/share/applications",
    "~/.local/share/applications"
  ],
  "cache_ttl": 1800,
  "theme": "dark"
}
```

### Enable Plugins

```bash
# Copy example plugins
cp -r spotlightx/plugins/examples/* ~/.config/spotlightx/plugins/

# Enable specific plugin
nano ~/.config/spotlightx/plugins/clipboard_history/plugin.json
# Set "enabled": true

# Restart
pkill -f spotlightx && cd spotlightx && python run.py
```

### Autostart on Login

#### Method 1: Desktop Entry

```bash
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/spotlightx.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=SpotlightX
Exec=/usr/bin/python3 /path/to/spotlightx/spotlightx/run.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

# Replace /path/to/spotlightx with actual path
sed -i "s|/path/to/spotlightx|$(pwd)|" ~/.config/autostart/spotlightx.desktop
```

#### Method 2: systemd User Service

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/spotlightx.service << EOF
[Unit]
Description=SpotlightX Launcher
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $(pwd)/spotlightx/run.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

# Enable service
systemctl --user enable spotlightx.service
systemctl --user start spotlightx.service

# Check status
systemctl --user status spotlightx.service
```

---

## Performance Tips

### 1. Reduce Indexing Scope

Edit `spotlightx/spotlightx/indexer.py`:

```python
# Change max_files
self.max_files = 5000  # instead of 20000

# Reduce search paths
self.file_roots = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
]
```

### 2. Use SSD for Cache

```bash
# If you have SSD, ensure cache is on SSD
df -h ~/.cache
```

### 3. Optimize Python

```bash
# Use PyPy for better performance (experimental)
pypy3 -m pip install -r requirements.txt
pypy3 run.py
```

---

## Development Workflow

### Recommended Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/spotlightx
cd spotlightx

# 2. Create branch
git checkout -b feature/my-feature

# 3. Setup venv
python3 -m venv venv
source venv/bin/activate

# 4. Install dev dependencies
pip install -r requirements.txt
pip install black flake8 mypy  # formatters/linters

# 5. Make changes
# Edit files...

# 6. Test
cd spotlightx && python run.py

# 7. Format code
black spotlightx/
flake8 spotlightx/

# 8. Commit
git add .
git commit -m "Add: my feature"
git push origin feature/my-feature
```

---

## Next Steps

- **Build Packages**: See [BUILD_GUIDE.md](BUILD_GUIDE.md)
- **Create Plugins**: See [PLUGIN_DEV_GUIDE.md](PLUGIN_DEV_GUIDE.md)
- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Quick Start**: See [QUICKSTART.md](../QUICKSTART.md)

---

**Copyright (c) 2025 WHO-AM-I-404**  
**Licensed under the MIT License**
