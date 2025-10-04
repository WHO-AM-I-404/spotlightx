# SpotlightX Build Guide

Complete guide to building SpotlightX from source code and creating distributable packages (AppImage & .deb).

## 📑 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Building from Source](#building-from-source)
4. [Building AppImage](#building-appimage)
5. [Building .deb Package](#building-deb-package)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **OS**: Debian 11+, Ubuntu 20.04+, or derivatives
- **Architecture**: x86_64 (amd64)
- **RAM**: 4 GB minimum
- **Disk**: 2 GB free space for build tools

### Required Tools

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Build essentials
sudo apt install -y build-essential gcc g++ make

# Git
sudo apt install -y git

# Qt6 dependencies (untuk PySide6)
sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 \
    libxkbcommon-x11-0

# Additional dependencies
sudo apt install -y xdg-utils file libmagic1
```

### Build Tools

#### PyInstaller

```bash
pip3 install pyinstaller
```

#### AppImageTool

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

#### FPM (untuk .deb)

```bash
sudo apt install -y ruby ruby-dev rubygems
sudo gem install --no-document fpm
```

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Development Version

```bash
cd spotlightx
python run.py
```

### 5. Test Functionality

```bash
# Test indexing
python -c "from spotlightx.indexer import Indexer; i = Indexer(); i.index_all()"

# Test search
python -c "from spotlightx.indexer import Indexer; from spotlightx.search import SearchEngine; i = Indexer(); s = SearchEngine(i); print(s.search('firefox'))"
```

## Building from Source

### Manual Build

#### 1. Build Executable with PyInstaller

```bash
# Activate venv
source venv/bin/activate

# Install PyInstaller
pip install pyinstaller

# Create spec file
cat > spotlightx.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['spotlightx/run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('spotlightx/spotlightx', 'spotlightx'),
        ('spotlightx/plugins', 'plugins'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'rapidfuzz',
        'watchdog',
        'pyperclip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='spotlightx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='spotlightx',
)
EOF

# Build
pyinstaller spotlightx.spec

# Test binary
./dist/spotlightx/spotlightx
```

#### 2. Optimize Binary

```bash
# Strip debug symbols
find dist/spotlightx -name "*.so" -exec strip {} \;

# Remove unnecessary files
rm -rf dist/spotlightx/{*.pyc,__pycache__}
find dist/spotlightx -name "*.pyo" -delete

# Compress with UPX (optional)
sudo apt install upx
find dist/spotlightx -type f -executable -exec upx --best {} \;
```

## Building AppImage

### Automated Script

```bash
./build/build_appimage.sh
```

### Manual Steps

#### 1. Create AppDir Structure

```bash
mkdir -p AppDir/usr/{bin,share/applications,share/icons/hicolor/256x256/apps}

# Copy binary
cp -r dist/spotlightx/* AppDir/usr/bin/

# Create wrapper script
cat > AppDir/usr/bin/spotlightx-wrapper.sh << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "${0}")")/../.."
export LD_LIBRARY_PATH="${APPDIR}/usr/lib:${LD_LIBRARY_PATH}"
exec "${APPDIR}/usr/bin/spotlightx" "$@"
EOF

chmod +x AppDir/usr/bin/spotlightx-wrapper.sh
```

#### 2. Create .desktop File

```bash
cat > AppDir/usr/share/applications/spotlightx.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=SpotlightX
GenericName=Application Launcher
Comment=Sophisticated and lightweight launcher for Linux
Exec=spotlightx
Icon=spotlightx
Categories=Utility;
Terminal=false
StartupNotify=true
Keywords=search;launcher;spotlight;
EOF
```

#### 3. Create Icon

```bash
# Create simple icon (atau gunakan custom icon)
convert -size 256x256 xc:blue \
    -gravity center -pointsize 72 -fill white -annotate +0+0 'SX' \
    AppDir/usr/share/icons/hicolor/256x256/apps/spotlightx.png
```

#### 4. Create AppRun

```bash
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "${0}")")"
export PATH="${APPDIR}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${APPDIR}/usr/lib:${LD_LIBRARY_PATH}"
exec "${APPDIR}/usr/bin/spotlightx" "$@"
EOF

chmod +x AppDir/AppRun
```

#### 5. Build AppImage

```bash
# Build
appimagetool AppDir SpotlightX-1.0.0-x86_64.AppImage

# Make executable
chmod +x SpotlightX-1.0.0-x86_64.AppImage

# Test
./SpotlightX-1.0.0-x86_64.AppImage
```

#### 6. Create Checksum

```bash
sha256sum SpotlightX-1.0.0-x86_64.AppImage > SpotlightX-1.0.0-x86_64.AppImage.sha256
```

### Size Optimization

```bash
# Typical size: 100-250 MB
# Optimize with:

# 1. Exclude unnecessary Qt modules
# Edit spotlightx.spec, add to excludes:
excludes=['PySide6.Qt3D', 'PySide6.QtWebEngine', ...]

# 2. Strip binaries
strip AppDir/usr/bin/spotlightx

# 3. Compress with UPX
upx --best AppDir/usr/bin/spotlightx

# 4. Remove locale files
rm -rf AppDir/usr/share/locale/*

# 5. Rebuild
appimagetool AppDir SpotlightX-1.0.0-x86_64.AppImage
```

## Building .deb Package

### Automated Script

```bash
./build/build_deb.sh
```

### Manual Steps with FPM

#### 1. Prepare Files

```bash
mkdir -p deb-package/usr/local/bin
mkdir -p deb-package/usr/share/applications
mkdir -p deb-package/usr/share/icons/hicolor/256x256/apps

# Copy binary
cp -r dist/spotlightx deb-package/usr/local/bin/

# Copy .desktop file
cp AppDir/usr/share/applications/spotlightx.desktop deb-package/usr/share/applications/

# Copy icon
cp AppDir/usr/share/icons/hicolor/256x256/apps/spotlightx.png \
   deb-package/usr/share/icons/hicolor/256x256/apps/
```

#### 2. Build with FPM

```bash
fpm -s dir -t deb \
    -n spotlightx \
    -v 1.0.0 \
    --iteration 1 \
    --architecture amd64 \
    --description "Sophisticated and lightweight launcher for Debian-based Linux" \
    --url "https://github.com/WHO-AM-I-404/spotlightx" \
    --license "MIT" \
    --maintainer "WHO-AM-I-404" \
    --depends "python3 (>= 3.11)" \
    --depends "libqt6widgets6" \
    --depends "libqt6gui6" \
    --depends "libqt6core6" \
    --depends "xdg-utils" \
    -C deb-package \
    usr/local/bin usr/share/applications usr/share/icons
```

#### 3. Test Package

```bash
# Install
sudo dpkg -i spotlightx_1.0.0-1_amd64.deb

# Test
spotlightx

# Uninstall
sudo dpkg -r spotlightx
```

### Alternative: debhelper

```bash
# Create debian/ directory structure
mkdir -p debian

# Create control file
cat > debian/control << 'EOF'
Source: spotlightx
Section: utils
Priority: optional
Maintainer: WHO-AM-I-404
Build-Depends: debhelper (>= 13), python3 (>= 3.11)
Standards-Version: 4.6.0

Package: spotlightx
Architecture: amd64
Depends: ${shlibs:Depends}, ${misc:Depends}, python3 (>= 3.11), libqt6widgets6, libqt6gui6, xdg-utils
Description: Sophisticated launcher for Linux
 SpotlightX is a lightweight and sophisticated application launcher
 for Debian-based Linux distributions.
EOF

# Create changelog
cat > debian/changelog << 'EOF'
spotlightx (1.0.0-1) stable; urgency=medium

  * Initial release

 -- WHO-AM-I-404  Sat, 04 Oct 2025 00:00:00 +0000
EOF

# Build
dpkg-buildpackage -us -uc -b
```

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/build.yml`:

```yaml
name: Build SpotlightX

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libxcb-cursor0 libxkbcommon-x11-0 xdg-utils
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        pyinstaller spotlightx.spec
    
    - name: Install AppImage tools
      run: |
        wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
        chmod +x appimagetool-x86_64.AppImage
        sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
    
    - name: Build AppImage
      run: |
        ./build/build_appimage.sh
    
    - name: Install FPM
      run: |
        sudo apt-get install -y ruby ruby-dev
        sudo gem install --no-document fpm
    
    - name: Build .deb
      run: |
        ./build/build_deb.sh
    
    - name: Create checksums
      run: |
        sha256sum SpotlightX*.AppImage > checksums.txt
        sha256sum spotlightx*.deb >> checksums.txt
    
    - name: Upload Release Assets
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: |
          SpotlightX*.AppImage
          spotlightx*.deb
          checksums.txt
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
image: ubuntu:22.04

stages:
  - build
  - package
  - release

build:
  stage: build
  script:
    - apt-get update && apt-get install -y python3.11 python3-pip
    - pip install -r requirements.txt
    - pip install pyinstaller
    - pyinstaller spotlightx.spec
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

package_appimage:
  stage: package
  dependencies:
    - build
  script:
    - ./build/build_appimage.sh
  artifacts:
    paths:
      - SpotlightX*.AppImage
    expire_in: 1 week

package_deb:
  stage: package
  dependencies:
    - build
  script:
    - apt-get install -y ruby ruby-dev
    - gem install --no-document fpm
    - ./build/build_deb.sh
  artifacts:
    paths:
      - spotlightx*.deb
    expire_in: 1 week
```

## Troubleshooting

### PyInstaller Issues

**Problem**: Missing modules

```bash
# Solution: Add to hiddenimports in spec file
hiddenimports=['module_name']
```

**Problem**: Qt plugins not found

```bash
# Solution: Include Qt plugins dir
datas=[
    ('/usr/lib/python3/dist-packages/PySide6/Qt/plugins', 'PySide6/Qt/plugins')
]
```

### AppImage Issues

**Problem**: AppImage won't run

```bash
# Check permissions
chmod +x SpotlightX.AppImage

# Check FUSE
sudo apt install fuse libfuse2

# Extract and run manually
./SpotlightX.AppImage --appimage-extract
./squashfs-root/AppRun
```

**Problem**: Missing libraries

```bash
# Check dependencies
ldd AppDir/usr/bin/spotlightx

# Copy missing libs
cp /usr/lib/x86_64-linux-gnu/libmissing.so AppDir/usr/lib/
```

### .deb Issues

**Problem**: Dependency errors

```bash
# Check dependencies
dpkg -I spotlightx.deb

# Fix broken dependencies
sudo apt --fix-broken install
```

**Problem**: postinst script errors

```bash
# Debug install
sudo dpkg -i --debug=1000 spotlightx.deb
```

## Performance Benchmarks

### Build Times

- **PyInstaller**: 2-5 minutes
- **AppImage**: 1-2 minutes
- **.deb**: 30 seconds - 1 minute
- **Total**: 5-10 minutes

### Package Sizes

- **PyInstaller dist/**: 80-150 MB
- **AppImage**: 100-250 MB
- **.deb**: 80-150 MB (unpacked)

### Optimization Results

| Optimization | Size Reduction |
|--------------|----------------|
| Strip binaries | -20 MB |
| Remove locales | -10 MB |
| UPX compression | -30-50 MB |
| Exclude Qt modules | -50-100 MB |

---

**Need Help?** [Report Issue](https://github.com/WHO-AM-I-404/spotlightx/issues)
