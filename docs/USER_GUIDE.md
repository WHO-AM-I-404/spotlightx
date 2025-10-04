# SpotlightX User Guide

Complete usage guide for SpotlightX end-users.

## 📑 Table of Contents

1. [Installation](#installation)
2. [First Run](#first-run)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Plugin Management](#plugin-management)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)

## Installation

### Method 1: AppImage (Recommended)

AppImage adalah format portable yang tidak memerlukan instalasi sistem. Cocok untuk semua distro Linux.

#### Download

```bash
# Download dari GitHub Releases
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/SpotlightX.AppImage

# Atau gunakan curl
curl -L -O https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/SpotlightX.AppImage
```

#### Setup

```bash
# Buat file executable
chmod +x SpotlightX.AppImage

# Optional: pindahkan ke ~/Applications
mkdir -p ~/Applications
mv SpotlightX.AppImage ~/Applications/

# Jalankan
~/Applications/SpotlightX.AppImage
```

#### Autostart (Optional)

Buat desktop entry untuk autostart:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/spotlightx.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=SpotlightX
Exec=/home/YOUR_USERNAME/Applications/SpotlightX.AppImage
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

Ganti `YOUR_USERNAME` dengan username Anda.

### Method 2: .deb Package

Cocok untuk Debian, Ubuntu, Linux Mint, dan turunannya.

#### Download & Install

```bash
# Download
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/spotlightx_1.0.0_amd64.deb

# Install
sudo dpkg -i spotlightx_1.0.0_amd64.deb

# Fix dependencies jika diperlukan
sudo apt --fix-broken install
```

#### Verifikasi Instalasi

```bash
# Check version
spotlightx --version

# Check location
which spotlightx
```

### Setup Global Hotkey

Untuk akses cepat dengan `Ctrl+Space`:

#### GNOME

```bash
# Via GUI
gnome-control-center keyboard

# Atau via command line
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'SpotlightX'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command 'spotlightx'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Primary>space'
```

#### KDE Plasma

1. Buka **System Settings** → **Shortcuts** → **Custom Shortcuts**
2. Edit → New → Global Shortcut → Command/URL
3. Trigger: `Ctrl+Space`
4. Action: `spotlightx` atau path ke AppImage

#### XFCE

1. Buka **Settings** → **Keyboard** → **Application Shortcuts**
2. Click **Add**
3. Command: `spotlightx`
4. Press `Ctrl+Space`

## First Run

### Initial Indexing

Saat pertama kali dijalankan, SpotlightX akan:

1. **Membuat direktori config** di `~/.config/spotlightx/`
2. **Membuat direktori cache** di `~/.cache/spotlightx/`
3. **Scan aplikasi** dari `/usr/share/applications`, `/usr/local/share/applications`, `~/.local/share/applications`
4. **Index files** dari Documents, Downloads, Desktop, Pictures, Videos

Proses ini memakan waktu 5-30 detik tergantung jumlah file.

### Verifikasi

```bash
# Check cache files
ls -lh ~/.cache/spotlightx/

# Expected output:
# apps.json    - Daftar aplikasi
# files.json   - Daftar file
# usage.json   - Usage statistics
```

## Basic Usage

### Membuka SpotlightX

**Keyboard**: Press `Ctrl+Space`

**Mouse/Terminal**: 
```bash
spotlightx
# atau
~/Applications/SpotlightX.AppImage
```

### Navigasi Keyboard

| Key | Action |
|-----|--------|
| `Ctrl+Space` | Toggle window (show/hide) |
| `Esc` | Hide window |
| `↑` `↓` | Navigate results |
| `Enter` | Open selected item |
| `Ctrl+L` | Focus search input |
| `Ctrl+C` | Quit application |

### Search Syntax

#### 1. Search Aplikasi

Ketik nama aplikasi:

```
firefox          → Mozilla Firefox
chrome           → Google Chrome
code             → Visual Studio Code
terminal         → GNOME Terminal
```

#### 2. Search File

Ketik nama file atau ekstensi:

```
report.pdf       → File bernama report.pdf
.jpg             → Semua file .jpg
invoice          → File yang mengandung "invoice"
```

#### 3. Kalkulator

Ketik ekspresi matematika:

```
2 + 2            → 4
(15 * 3) / 2     → 22.5
100 * 1.5        → 150.0
50 - 10 * 2      → 30
```

Hasil akan otomatis disalin ke clipboard.

#### 4. Open URL

Ketik URL:

```
github.com
https://example.com
www.google.com
```

#### 5. Web Search Shortcuts

| Shortcut | Service | Example |
|----------|---------|---------|
| `g` | Google | `g python tutorial` |
| `yt` | YouTube | `yt music video` |
| `ddg` | DuckDuckGo | `ddg privacy tools` |
| `gh` | GitHub | `gh spotlightx` |
| `so` | Stack Overflow | `so python async` |
| `wiki` | Wikipedia | `wiki linux kernel` |

## Advanced Features

### Fuzzy Matching

SpotlightX menggunakan fuzzy matching, jadi Anda tidak perlu mengetik nama lengkap:

```
ffx      → Firefox
chr      → Chrome
vsc      → Visual Studio Code
gth      → GitHub Desktop
```

### Usage Ranking

Items yang sering digunakan akan muncul lebih tinggi di hasil pencarian:

- **Boost otomatis** berdasarkan frekuensi penggunaan
- **Recent boost** untuk items yang baru dibuka
- **Smart ranking** yang belajar dari kebiasaan Anda

### Background Indexing

Indexer berjalan di background dan refresh otomatis:

- **Initial index** saat aplikasi start
- **Periodic refresh** setiap 30 menit
- **Manual refresh** via restart aplikasi

### Refresh Index

Jika ada aplikasi atau file baru yang tidak muncul:

```bash
# Restart aplikasi
pkill -f spotlightx
spotlightx

# Atau clear cache
rm -rf ~/.cache/spotlightx/*
spotlightx
```

## Plugin Management

### Plugin Location

Plugins disimpan di:
```
~/.config/spotlightx/plugins/
```

### Enable Plugin

1. Copy plugin folder ke `~/.config/spotlightx/plugins/`
2. Edit `plugin.json`, set `"enabled": true`
3. Restart SpotlightX

Contoh:
```bash
cp -r ~/Downloads/my_plugin ~/.config/spotlightx/plugins/
nano ~/.config/spotlightx/plugins/my_plugin/plugin.json
# Set "enabled": true
pkill -f spotlightx && spotlightx
```

### Disable Plugin

Edit `plugin.json`, set `"enabled": false`:

```bash
nano ~/.config/spotlightx/plugins/my_plugin/plugin.json
# Set "enabled": false
```

### Built-in Example Plugins

SpotlightX menyertakan 10 plugin contoh di `spotlightx/plugins/examples/`:

1. **Clipboard History** (`clip search_term`)
   ```
   clip password    → Search clipboard for "password"
   clip             → Show all clipboard history
   ```

2. **Translator** (`tr text`)
   ```
   tr hello world   → Translate via Google Translate
   ```

3. **Battery Notifier** (`battery`)
   ```
   battery          → Show battery status
   bat              → Battery percentage
   ```

4. **Focus Mode** (`focus`)
   ```
   focus            → Toggle focus/DND mode
   dnd              → Toggle Do Not Disturb
   ```

5. **Timeline** (`timeline`)
   ```
   timeline         → Show recent activity
   history          → Activity history
   recent           → Recently opened items
   ```

6. **File Preview** (`preview filename`)
   ```
   preview /path/to/file.txt   → Preview text content
   ```

7. **Web Shortcuts** (Extended)
   ```
   reddit python    → Search Reddit
   tw linux         → Search Twitter
   maps jakarta     → Google Maps
   ```

### Copy Example Plugins

```bash
# Copy semua plugins
cp -r /path/to/spotlightx/spotlightx/plugins/examples/* ~/.config/spotlightx/plugins/

# Enable plugin tertentu
nano ~/.config/spotlightx/plugins/clipboard_history/plugin.json
# Set "enabled": true
```

## Configuration

### Config File Location

Main config (future): `~/.config/spotlightx/config.json`

Plugin configs: `~/.config/spotlightx/plugins/<plugin_id>/config.json`

### Customize Search Roots

Edit file indexer untuk customize search paths:

```bash
nano ~/.config/spotlightx/config.json
```

```json
{
  "file_roots": [
    "~/Documents",
    "~/Downloads",
    "~/Projects",
    "/mnt/data"
  ],
  "max_results": 15,
  "cache_ttl": 1800
}
```

### Theme (Future Feature)

Default theme adalah dark. Custom theme akan tersedia di versi mendatang.

## Troubleshooting

### Aplikasi Tidak Muncul

**Problem**: Aplikasi terinstall tapi tidak muncul di hasil

**Solution**:
```bash
# Check .desktop files
ls ~/.local/share/applications/
ls /usr/share/applications/

# Refresh index
rm ~/.cache/spotlightx/apps.json
spotlightx
```

### File Tidak Terindex

**Problem**: File ada tapi tidak muncul

**Solution**:
```bash
# Check file locations
ls ~/Documents
ls ~/Downloads

# Clear file cache
rm ~/.cache/spotlightx/files.json

# Check permissions
ls -la ~/Documents
```

### Hotkey Tidak Berfungsi

**Problem**: `Ctrl+Space` tidak membuka SpotlightX

**Solution X11**:
```bash
# Install python-xlib
pip install python-xlib

# Restart SpotlightX
pkill -f spotlightx && spotlightx
```

**Solution Wayland**:
Set manual keyboard shortcut (see section Setup Global Hotkey)

### High Memory Usage

**Problem**: Memory > 200 MB

**Solution**:
```bash
# Limit indexed files
# Edit config untuk reduce file_roots

# Clear old cache
rm -rf ~/.cache/spotlightx/*

# Restart
pkill -f spotlightx && spotlightx
```

### Window Tidak Muncul

**Problem**: No window visible setelah jalankan

**Solution**:
```bash
# Check logs
journalctl --user -f | grep spotlightx

# Check dependencies
ldd ~/Applications/SpotlightX.AppImage

# For .deb install
sudo apt install --reinstall libqt6widgets6 libqt6gui6
```

### Plugin Error

**Problem**: Plugin causing crashes

**Solution**:
```bash
# Disable semua plugins
for plugin in ~/.config/spotlightx/plugins/*/plugin.json; do
    sed -i 's/"enabled": true/"enabled": false/' "$plugin"
done

# Enable one by one untuk identify problem
```

### Performance Issues

**Problem**: Slow search atau high CPU

**Solution**:
```bash
# Reduce indexed files
nano ~/.config/spotlightx/config.json
# Set smaller file_roots

# Increase cache TTL
# Set "cache_ttl": 3600

# Disable heavy plugins
```

## Tips & Tricks

### 1. Quick Calculator

Gunakan SpotlightX sebagai calculator cepat:
```
100 * 15 / 2    → Hasil langsung
```

### 2. Web Research

Combine web shortcuts untuk research cepat:
```
g quantum computing      → Google
wiki quantum computing   → Wikipedia
yt quantum computing     → YouTube videos
```

### 3. File Organization

Gunakan Timeline plugin untuk track frequently used files:
```
timeline    → See your most used files
```

### 4. Clipboard Management

Enable Clipboard History plugin untuk productivity:
```
clip password    → Find saved password
clip code        → Find code snippet
```

### 5. Battery Monitoring

Quick battery check without opening settings:
```
battery    → Instant battery status
```

## FAQ

### Q: Apakah SpotlightX memerlukan root access?

A: Tidak. SpotlightX berjalan sebagai user application dan tidak memerlukan sudo/root.

### Q: Berapa memory yang digunakan?

A: 30-120 MB idle, tergantung jumlah indexed items dan enabled plugins.

### Q: Apakah data saya aman?

A: Ya. SpotlightX:
- Tidak mengirim data ke internet
- Semua cache local
- No telemetry
- Open source code

### Q: Bisa digunakan di Wayland?

A: Ya, dengan manual hotkey setup. X11 support auto hotkey.

### Q: Support distro apa saja?

A: Debian, Ubuntu, Linux Mint, Pop!_OS, Elementary OS, dan Debian-based lainnya.

### Q: Bisa custom UI theme?

A: Saat ini default dark theme. Custom theme akan ada di version mendatang.

---

**Need Help?** [Report Issue](https://github.com/WHO-AM-I-404/spotlightx/issues) or join [Discussions](https://github.com/WHO-AM-I-404/spotlightx/discussions)
