# 📋 SpotlightX - Version History & Release Notes

Complete documentation of changes and version history for SpotlightX.

---

## 📊 Version Overview

| Version | Release Date | Type | Status |
|---------|-------------|------|--------|
| [1.1.0](#version-110) | 2025-10-04 | Minor | **Current** ✨ |
| [1.0.0](#version-100) | 2025-10-04 | Major | Stable |

**Current Version**: `1.1.0`  
**Latest Release**: October 4, 2025

---

## 🔄 Semantic Versioning Guide

SpotlightX uses [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─── Bug fixes (backwards compatible)
  │     └───────── New features (backwards compatible)
  └─────────────── Breaking changes (incompatible)
```

### Versioning Examples:
- **1.0.0 → 1.0.1**: Minor bug fix (PATCH)
- **1.0.1 → 1.1.0**: New feature (MINOR) ← **Current update**
- **1.9.9 → 2.0.0**: Breaking changes that are incompatible (MAJOR)

---

## 📦 Version 1.1.0 - Enhanced Search & Tooling

**Release Date**: October 4, 2025  
**Type**: Minor Update  
**Download**: [GitHub Releases](https://github.com/WHO-AM-I-404/spotlightx/releases/tag/v1.1.0)

### 🎯 Update Focus

This update improves search capabilities and simplifies the application build/distribution process.

### ✨ New Features

#### 1. Enhanced File Indexing
- **20,000 files** (up from 10,000 files)
- **Depth 4 levels** (up from 3 levels)
- Support for **Snap applications**
- Support for **Flatpak applications** (system & user)
- Indexing **~/Music** folder
- Indexing home directory root **~/**

#### 2. File Utilities Module
New module for better file handling:
```python
from spotlightx.utils import get_file_type, format_file_size

get_file_type("document.pdf")  # → "PDF Document"
format_file_size(1024000)      # → "1000.0 KB"
```

#### 3. Improved Search Results Display
File search results now show:
- **File Type**: "PDF Document", "JPEG Image", etc.
- **File Size**: Human-readable format (KB, MB, GB)
- **Full Path**: Complete file location

**Before (v1.0.0)**:
```
report.pdf
/home/user/Documents/report.pdf
```

**After (v1.1.0)**:
```
report.pdf
PDF Document — 2.5 MB — /home/user/Documents/report.pdf
```

#### 4. Automated Build Scripts
Two ready-to-use build scripts:

**build_appimage.sh**:
```bash
./build/build_appimage.sh
# Output: SpotlightX-1.1.0-x86_64.AppImage
```

**build_deb.sh**:
```bash
./build/build_deb.sh
# Output: spotlightx_1.1.0-1_amd64.deb
```

#### 5. Complete Plugin System
10 complete example plugins with documentation:
1. **Clipboard History** - Manage clipboard entries
2. **Translator** - Quick translation via web
3. **Battery Notifier** - Battery status monitoring
4. **Focus Mode** - Toggle Do Not Disturb
5. **Context Menu Enhancer** - File quick actions
6. **Spotlight Timeline** - Activity tracking
7. **File Preview** - Quick file preview
8. **Drag & Drop Integration** - Drag & drop helpers
9. **Settings Sync** - Config backup/sync
10. **Web Search Shortcuts** - Extended web shortcuts

### 🔧 Improvements

#### Performance
- More files indexed → more comprehensive search
- Deeper depth → find hidden files in subfolders

#### Compatibility
- **Snap Apps**: Support for applications installed via Snap
- **Flatpak Apps**: Support for applications installed via Flatpak
- **Modern Package Managers**: Compatible with various app installation methods

#### Developer Experience
- Automated build scripts → easier building
- Better type hints → LSP errors fixed
- Improved module structure → better organized code

### 📝 Changed

| Component | Old | New |
|-----------|-----|-----|
| Max indexed files | 10,000 | 20,000 |
| Search depth | 3 levels | 4 levels |
| App search paths | 3 paths | 6 paths |
| File search paths | 5 folders | 7 folders |

### 🐛 Fixed

- Type hints issues (LSP diagnostics)
- Uninformative file subtitles
- Missing support for modern app formats

### 📦 Package Information

**AppImage**:
- File: `SpotlightX-1.1.0-x86_64.AppImage`
- Estimated size: ~100-250 MB
- Platform: x86_64 Linux

**Debian Package**:
- File: `spotlightx_1.1.0-1_amd64.deb`
- Architecture: amd64
- Dependencies: python3 (>= 3.9), xdg-utils

### 📥 Download Links

```bash
# AppImage
wget https://github.com/WHO-AM-I-404/spotlightx/releases/download/v1.1.0/SpotlightX-1.1.0-x86_64.AppImage

# Debian Package
wget https://github.com/WHO-AM-I-404/spotlightx/releases/download/v1.1.0/spotlightx_1.1.0-1_amd64.deb
```

### 🔄 Upgrade from v1.0.0

**AppImage Users**:
```bash
# Download new version
wget https://github.com/WHO-AM-I-404/spotlightx/releases/download/v1.1.0/SpotlightX-1.1.0-x86_64.AppImage
chmod +x SpotlightX-1.1.0-x86_64.AppImage

# Delete old version (optional)
rm SpotlightX-1.0.0-x86_64.AppImage
```

**Debian Package Users**:
```bash
# Download and install new version
wget https://github.com/WHO-AM-I-404/spotlightx/releases/download/v1.1.0/spotlightx_1.1.0-1_amd64.deb
sudo dpkg -i spotlightx_1.1.0-1_amd64.deb
```

Cache and config will remain saved in:
- `~/.cache/spotlightx/`
- `~/.config/spotlightx/`

---

## 📦 Version 1.0.0 - Initial Release

**Release Date**: October 4, 2025  
**Type**: Major Release (Initial)  
**Download**: [GitHub Releases](https://github.com/WHO-AM-I-404/spotlightx/releases/tag/v1.0.0)

### 🎯 Initial Release Highlights

First release of SpotlightX with complete core features.

### ✨ Core Features

#### 1. Search Engine
- **Fuzzy Matching**: Smart search with rapidfuzz
- **Multi-source**: Apps, files, calculator, URLs, web shortcuts
- **Smart Ranking**: Based on relevance, usage, and recency

#### 2. Application Indexing
Scan and index applications from:
- `/usr/share/applications`
- `/usr/local/share/applications`
- `~/.local/share/applications`

#### 3. File Indexing
Index files from directories:
- `~/Documents`
- `~/Downloads`
- `~/Desktop`
- `~/Pictures`
- `~/Videos`

**Specs**:
- Max files: 10,000
- Search depth: 3 levels
- Cache: JSON format in `~/.cache/spotlightx/`

#### 4. Calculator
Safe mathematical expression evaluation:
```
2 + 2              → 4
(15 * 3) / 2       → 22.5
100 * 1.5          → 150.0
```

Results are automatically copied to clipboard!

#### 5. Web Integration

**Direct URL**:
```
github.com         → Opens in browser
https://example.com
```

**Web Shortcuts**:
```
g python           → Google search
yt music           → YouTube search
ddg privacy        → DuckDuckGo
gh awesome         → GitHub search
so python async    → Stack Overflow
wiki linux         → Wikipedia
```

#### 6. User Interface
- **Tkinter UI**: Lightweight fallback
- **Dark Theme**: Default
- **Keyboard Navigation**: Full support
- **Animations**: Smooth fade in/out

#### 7. Plugin System

**Architecture**:
- Hook-based system
- Sandboxed execution
- Config management
- Opt-in activation

**Available Hooks**:
- `on_query`: Add custom results
- `on_open`: React to selections
- `on_startup`: Initialize plugin
- `on_shutdown`: Cleanup

#### 8. Safe Execution
- ✅ No `shell=True` execution
- ✅ .desktop Exec field parsing
- ✅ xdg-open integration
- ✅ No root required

#### 9. Usage Tracking
- Frequency counting
- Recency tracking
- Smart ranking boost
- Stored in `~/.cache/spotlightx/usage.json`

#### 10. Background Indexing
- Non-blocking initial scan
- Periodic refresh (every 30 minutes)
- Manual refresh on restart

### 📊 Technical Specifications

**System Requirements**:
- OS: Debian 11+, Ubuntu 20.04+
- Python: 3.11+
- RAM: 2 GB minimum
- Disk: 200 MB

**Performance**:
- Memory usage: 30-120 MB idle
- Cache size: < 5 MB
- Startup time: < 2 seconds
- Search latency: < 50ms

**Dependencies**:
- PySide6 (UI)
- rapidfuzz (search)
- watchdog (file monitoring)
- python-xlib (X11 hotkey)
- pyperclip (clipboard)

### 📦 Package Information

**AppImage**:
- File: `SpotlightX-1.0.0-x86_64.AppImage`
- Portable, single-file
- No installation needed

**Debian Package**:
- File: `spotlightx_1.0.0-1_amd64.deb`
- Native installation
- System integration

### 🎓 Documentation

Complete documentation included:
- README.md - Overview
- USER_GUIDE.md - User manual
- PLUGIN_DEV_GUIDE.md - Plugin development
- BUILD_GUIDE.md - Build instructions
- RUNNING_FROM_SOURCE.md - Developer guide

---

## 🗓️ Release Timeline

```
2025-10-04: v1.1.0 - Enhanced Search & Tooling
2025-10-04: v1.0.0 - Initial Release
```

---

## 🔮 Future Roadmap

### Version 1.2.0 (Planned)
**Target**: Q4 2025  
**Type**: Minor Update

**Planned Features**:
- [ ] PySide6/QML production UI
- [ ] Glass/blur effects
- [ ] Smooth animations (Qt)
- [ ] X11 hotkey auto-registration
- [ ] Real-time file watching (inotify)
- [ ] Advanced file preview
- [ ] Thumbnail generation
- [ ] Custom themes support

### Version 1.3.0 (Planned)
**Target**: Q1 2026  
**Type**: Minor Update

**Planned Features**:
- [ ] Plugin marketplace
- [ ] One-click plugin installation
- [ ] Plugin rating system
- [ ] Auto-update for plugins
- [ ] Better plugin sandboxing

### Version 2.0.0 (Planned)
**Target**: Q2 2026  
**Type**: Major Update

**Planned Features**:
- [ ] Wayland native support
- [ ] Auto-update mechanism
- [ ] Multi-language UI (i18n)
- [ ] Cloud sync integration
- [ ] AI-powered search suggestions
- [ ] Voice commands (optional)
- [ ] Mobile companion app

---

## 📈 Statistics

### Version 1.1.0 vs 1.0.0

| Metric | v1.0.0 | v1.1.0 | Change |
|--------|--------|--------|--------|
| Max Indexed Files | 10,000 | 20,000 | +100% |
| Search Depth | 3 levels | 4 levels | +33% |
| App Search Paths | 3 | 6 | +100% |
| File Search Paths | 5 | 7 | +40% |
| Example Plugins | 0 | 10 | New |
| Build Scripts | 0 | 2 | New |
| Documentation Files | 5 | 8 | +60% |

---

## 🤝 Contributing

Want to contribute? Check out the development version in the `develop` branch:

```bash
git clone https://github.com/WHO-AM-I-404/spotlightx
git checkout develop
```

**Contribution Guidelines**:
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👤 Maintainer

**WHO-AM-I-404**

- GitHub: [@WHO-AM-I-404](https://github.com/WHO-AM-I-404)
- Project: [SpotlightX](https://github.com/WHO-AM-I-404/spotlightx)

---

## 🙏 Acknowledgments

Thanks to all libraries and tools:
- PySide6/Qt Framework
- rapidfuzz for fuzzy matching
- python-xlib for X11 integration
- watchdog for file monitoring
- All contributors and users!

---

**Last Updated**: October 4, 2025  
**Document Version**: 1.1.0

**Copyright (c) 2025 WHO-AM-I-404 | Licensed under the MIT License**
