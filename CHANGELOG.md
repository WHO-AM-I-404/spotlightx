# Changelog

All notable changes to SpotlightX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-04

### Added
- **Enhanced File Search**: Increased indexed files from 10,000 to 20,000 files
- **Deeper Directory Scanning**: Search depth increased from 3 to 4 levels
- **Additional Search Paths**: 
  - Snap applications support (`/var/lib/snapd/desktop/applications`)
  - Flatpak applications support (system & user)
  - Music folder indexing (`~/Music`)
  - Home directory root search (`~`)
- **File Utilities Module**: New utility functions for better file handling
  - File type detection with human-readable names (PDF Document, JPEG Image, etc.)
  - File size formatting (B, KB, MB, GB, TB)
  - Enhanced file pattern matching
- **Improved Search Results**: File results now show:
  - File type (e.g., "PDF Document", "PNG Image")
  - File size in human-readable format
  - Full file path
- **Build Scripts**: Automated build scripts for easy packaging
  - `build/build_appimage.sh` - Build portable AppImage
  - `build/build_deb.sh` - Build Debian package
- **10 Example Plugins**: Complete plugin system with examples
  - Clipboard History
  - Translator
  - Battery Notifier
  - Focus Mode
  - Context Menu Enhancer
  - Spotlight Timeline
  - File Preview
  - Drag & Drop Integration
  - Settings Sync
  - Web Search Shortcuts

### Changed
- File search subtitle now includes file type and size
- Indexer now scans more application directories
- Better support for modern app distribution methods (Snap, Flatpak)

### Fixed
- Type hints for better IDE support
- LSP diagnostics errors resolved

## [1.0.0] - 2025-10-04

### Added
- **Initial Release** of SpotlightX
- **Core Search Engine**: Fuzzy matching with rapidfuzz
- **Application Indexing**: Scan .desktop files from standard locations
- **File Indexing**: Index common user directories (Documents, Downloads, Desktop, Pictures, Videos)
- **Calculator**: Safe mathematical expression evaluation
- **Web Integration**:
  - Direct URL opening
  - Web search shortcuts (Google, YouTube, DuckDuckGo, GitHub, Stack Overflow, Wikipedia)
- **Tkinter UI**: Lightweight fallback UI for development
- **Plugin System**: Extensible architecture with hooks
  - `on_query`: Custom search results
  - `on_open`: Action triggers
  - `on_startup`: Initialization
  - `on_shutdown`: Cleanup
- **Safe Executor**: No shell injection vulnerabilities
  - Secure .desktop Exec parsing
  - xdg-open integration
- **Usage Tracking**: Smart ranking based on frequency and recency
- **Background Indexing**: Non-blocking initial and periodic refresh
- **Cache System**: JSON-based caching in `~/.cache/spotlightx/`
- **Configuration**: Plugin configs in `~/.config/spotlightx/`

### Technical Specifications
- Python 3.11+ support
- PySide6/Qt6 ready (with Tkinter fallback)
- Memory usage: 30-120 MB idle
- Cache size: < 5 MB
- Support for Debian-based distributions

### Security
- No root access required
- No shell command execution with user input
- Safe evaluation for calculator
- Sandboxed plugin execution

---

## Version Numbering Guide

SpotlightX follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

### Examples:
- `1.0.0` → `1.0.1`: Bug fix (PATCH)
- `1.0.1` → `1.1.0`: New feature (MINOR)
- `1.9.9` → `2.0.0`: Breaking change (MAJOR)

---

## Future Roadmap

### Planned for v1.2.0
- [ ] PySide6/QML production UI with glass effects
- [ ] X11 hotkey auto-registration
- [ ] Real-time file watching with inotify
- [ ] Advanced file preview with thumbnails
- [ ] Custom themes support

### Planned for v2.0.0
- [ ] Wayland native support
- [ ] Auto-update mechanism
- [ ] Plugin marketplace
- [ ] Multi-language support
- [ ] Cloud sync integration

---

**Note**: For detailed changes in each version, see the git commit history.
