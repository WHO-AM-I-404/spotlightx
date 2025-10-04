# SpotlightX

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)

**SpotlightX** is a sophisticated, lightweight, and secure launcher/spotlight application for Debian-based Linux distributions. Equipped with an extensible plugin system, modern UI with glass/translucency effects, and easy packaging (AppImage & .deb).

## 🌟 Key Features

### Core Features
- **🔍 Fast Search** with fuzzy matching using rapidfuzz
  - Applications (.desktop files)
  - Files & folders (Documents, Downloads, Desktop, Pictures, Videos)
  - Instant math calculator
  - URL & web search shortcuts
- **⚡ Lightweight Performance**
  - Memory usage: 30-120 MB idle
  - Cache size: < 5 MB
  - Fast indexing with background threads
- **🎨 Modern UI**
  - Glass/translucency effects
  - Smooth fade in/out animations
  - Dark theme by default
  - Full keyboard navigation
- **🔐 Security**
  - No shell injection (no `shell=True`)
  - Safe .desktop Exec parsing
  - Plugin sandboxing
  - Per-user configuration (no root required)

### Plugin System (10 Plugins)
1. **Clipboard History** - Store & re-paste clipboard entries
2. **Translator** - Text translation via web services
3. **Battery Notifier** - Monitor battery status
4. **Focus Mode** - Toggle Do Not Disturb
5. **Context Menu Enhancer** - Quick actions for results
6. **Spotlight Timeline** - Record activity & frequency ranking
7. **File Preview** - Quick preview of images/text/PDF
8. **Drag & Drop Integration** - Helper for drag & drop operations
9. **Settings Sync** - Synchronize settings
10. **Web Search Shortcuts** - Extended web shortcuts

### Distribution
- **AppImage** (portable, single file, recommended)
- **.deb package** (native installation for Debian/Ubuntu)

## 📦 Installation

### Method 1: Run from Source (Development)

Perfect for developers and contributors:

```bash
# Clone repository
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx

# Install dependencies
pip install -r requirements.txt

# Run directly
cd spotlightx
python run.py
```

**See complete guide**: [Running from Source](docs/RUNNING_FROM_SOURCE.md)

### Method 2: AppImage (Recommended for End Users)

```bash
# Download AppImage
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/SpotlightX.AppImage

# Make executable
chmod +x SpotlightX.AppImage

# Run
./SpotlightX.AppImage
```

### Method 3: .deb Package

```bash
# Download .deb package
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/spotlightx_1.1.0_amd64.deb

# Install
sudo dpkg -i spotlightx_1.1.0_amd64.deb

# Fix dependencies if any
sudo apt --fix-broken install

# Run
spotlightx
```

### Setup Global Hotkey (Ctrl+Space)

#### X11 (Auto)
For X11, the hotkey will auto-register using python-xlib.

#### Wayland (Manual)
For Wayland, add a custom keyboard shortcut:

1. Open **Settings** → **Keyboard** → **Custom Shortcuts**
2. Click **Add Custom Shortcut**
3. Name: `SpotlightX`
4. Command: `/path/to/SpotlightX.AppImage` or `spotlightx`
5. Shortcut: `Ctrl+Space`

## 🚀 Usage

### Keyboard Shortcuts
- **Ctrl+Space** - Toggle SpotlightX window
- **Esc** - Hide window
- **Up/Down** - Navigate results
- **Enter** - Open selected item
- **Ctrl+L** - Focus search input

### Search Examples

#### Applications
```
firefox
chrome
code
```

#### Files
```
report.pdf
vacation.jpg
```

#### Calculator
```
2 + 2
(15 * 3) / 2
100 * 1.5
```

#### Web Search
```
g python tutorial        → Google search
yt react hooks          → YouTube search
ddg privacy tools       → DuckDuckGo search
gh spotlightx          → GitHub search
```

#### URL
```
github.com
https://example.com
```

#### Plugin Commands
```
clip search term        → Search clipboard history
battery                → Show battery status
timeline               → Show activity timeline
tr hello world         → Translate text
```

## 🔌 Plugin Development

See [PLUGIN_DEV_GUIDE.md](docs/PLUGIN_DEV_GUIDE.md) for complete documentation on how to create plugins.

### Quick Example

1. Create plugin folder at `~/.config/spotlightx/plugins/my_plugin/`
2. Create `plugin.json`:
```json
{
  "id": "my_plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "enabled": true
}
```

3. Create `plugin.py`:
```python
def on_query(query: str):
    if query.startswith('hello'):
        return [{
            'type': 'info',
            'name': 'Hello World!',
            'subtitle': 'My custom result',
            'action': '',
            'score': 900
        }]

def register(plugin_manager):
    plugin_manager.register_hook('on_query', on_query)
```

## 🛠️ Build from Source

### Requirements
```bash
# Python 3.11+
sudo apt install python3.11 python3.11-venv

# Dependencies
sudo apt install libxcb-cursor0 libxkbcommon-x11-0 xdg-utils

# Build tools
sudo apt install ruby ruby-dev gcc make
sudo gem install fpm
```

### Build AppImage

```bash
# Clone repository
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build
./build/build_appimage.sh
```

### Build .deb Package

```bash
./build/build_deb.sh
```

See [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) for complete documentation.

## 📊 Technical Specifications

### Performance
- **Startup time**: < 2 seconds
- **Search latency**: < 50ms for 10k items
- **Memory usage**: 30-120 MB idle
- **Cache size**: < 5 MB

### File Locations
- **Config**: `~/.config/spotlightx/`
- **Cache**: `~/.cache/spotlightx/`
- **Plugins**: `~/.config/spotlightx/plugins/`

### Supported Systems
- **OS**: Debian, Ubuntu, Linux Mint, Pop!_OS, Elementary OS
- **Display Server**: X11 (full support), Wayland (manual hotkey)
- **Architecture**: x86_64 (amd64)

## 📚 Complete Documentation

- [📖 User Guide](docs/USER_GUIDE.md) - Complete usage guide
- [🔌 Plugin Development Guide](docs/PLUGIN_DEV_GUIDE.md) - Create custom plugins
- [🏗️ Build Guide](docs/BUILD_GUIDE.md) - Build AppImage & .deb
- [💻 Running from Source](docs/RUNNING_FROM_SOURCE.md) - Developer guide
- [⚡ Quick Start](QUICKSTART.md) - Get started in 5 minutes
- [📋 Changelog](CHANGELOG.md) - Version history and changes

## 🤝 Contributing

Contributions are very welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author

**WHO-AM-I-404**

## 🙏 Credits

- **PySide6/Qt** - UI framework
- **rapidfuzz** - Fuzzy string matching
- **python-xlib** - X11 hotkey registration
- **Watchdog** - File system monitoring

## 📧 Support

If you have questions or issues:

- 🐛 [Report Bug](https://github.com/WHO-AM-I-404/spotlightx/issues)
- 💡 [Request Feature](https://github.com/WHO-AM-I-404/spotlightx/issues)
- 💬 [Discussions](https://github.com/WHO-AM-I-404/spotlightx/discussions)

---

**Made with ❤️ by WHO-AM-I-404**

**Copyright (c) 2025 WHO-AM-I-404 | Licensed under the MIT License**
