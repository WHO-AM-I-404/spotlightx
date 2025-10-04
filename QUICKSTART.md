# 🚀 SpotlightX - Quick Start Guide for Beginners

A short and easy guide to get started with SpotlightX.

---

## 📖 What is SpotlightX?

SpotlightX is a **fast search app** for Linux that helps you:
- 🔍 Quickly search for applications (like Firefox, Chrome, VSCode)
- 📁 Find files and folders on your computer
- 🧮 Calculate math instantly
- 🌐 Open websites and search on Google/YouTube

**Like Spotlight on Mac** or **Search on Windows**, but for Linux!

---

## ⚡ How to Install (3 Minutes)

### Option 1: Download AppImage File (EASIEST)

```bash
# 1. Download file
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/SpotlightX-1.1.0-x86_64.AppImage

# 2. Make it executable
chmod +x SpotlightX-1.1.0-x86_64.AppImage

# 3. Run!
./SpotlightX-1.1.0-x86_64.AppImage
```

**Done!** 🎉

### Option 2: Install .deb Package (for Ubuntu/Debian)

```bash
# 1. Download
wget https://github.com/WHO-AM-I-404/spotlightx/releases/latest/download/spotlightx_1.1.0-1_amd64.deb

# 2. Install
sudo dpkg -i spotlightx_1.1.0-1_amd64.deb

# 3. Run
spotlightx
```

---

## 🎯 How to Use (Super Simple!)

### 1. Open SpotlightX

Click the application or run in terminal:
```bash
./SpotlightX-1.1.0-x86_64.AppImage
```
or
```bash
spotlightx
```

### 2. Start Searching!

**A window will appear in the center of the screen**. Just type what you're looking for:

#### Example 1: Search Applications
```
Type: firefox
→ Press Enter
→ Firefox will open!
```

#### Example 2: Search Files
```
Type: report.pdf
→ Press Enter
→ PDF file will open!
```

#### Example 3: Calculator
```
Type: 15 * 20
→ Result: 300
→ Automatically copied to clipboard!
```

#### Example 4: Open Website
```
Type: github.com
→ Press Enter
→ Browser opens to GitHub!
```

#### Example 5: Google Search
```
Type: g python tutorial
→ Press Enter
→ Google search for "python tutorial"!
```

### 3. Keyboard Shortcuts

| Key | Function |
|--------|--------|
| `↑` `↓` | Navigate up/down |
| `Enter` | Open selected item |
| `Esc` | Close window |

**Simple, right?** 😊

---

## 🔥 Pro Tips

### 1. Web Search Shortcuts

```
g python              → Google search
yt music video        → YouTube search
ddg privacy tools     → DuckDuckGo search
gh awesome-python     → GitHub search
wiki linux            → Wikipedia search
```

### 2. Fuzzy Search (Don't Need to Type Complete)

```
ffx     → Firefox
chr     → Chrome
vsc     → Visual Studio Code
```

### 3. File Search by Type

```
.pdf    → All PDF files
.jpg    → All JPG images
.mp3    → All music files
```

---

## ⚙️ Setup Hotkey (Optional but Recommended!)

To open SpotlightX with `Ctrl+Space` (like Mac):

### Ubuntu/GNOME:

1. Open **Settings** → **Keyboard** → **Keyboard Shortcuts**
2. Scroll down, click **"+"** (Add Custom Shortcut)
3. Fill in:
   - **Name**: `SpotlightX`
   - **Command**: `/path/to/SpotlightX-1.1.0-x86_64.AppImage`
   - **Shortcut**: Press `Ctrl+Space`
4. Click **Add**

### KDE Plasma:

1. **System Settings** → **Shortcuts** → **Custom Shortcuts**
2. **Edit** → **New** → **Global Shortcut** → **Command/URL**
3. **Trigger**: `Ctrl+Space`
4. **Action**: `/path/to/SpotlightX-1.1.0-x86_64.AppImage`

Now just press `Ctrl+Space` anytime to open SpotlightX! 🎉

---

## 🏗️ Build from Source (for Developers)

Want to build it yourself? Easy!

### 1. Clone Repository

```bash
git clone https://github.com/WHO-AM-I-404/spotlightx
cd spotlightx
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# or use uv (faster)
uv pip install -r requirements.txt
```

### 3. Run Development Mode

```bash
cd spotlightx
python run.py
```

**Window will appear!** The app runs directly from source code.

### 4. Build AppImage (Optional)

```bash
# Install build tools
pip install pyinstaller

# Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool

# Build!
./build/build_appimage.sh
```

**Output**: `SpotlightX-1.1.0-x86_64.AppImage` ✅

### 5. Build .deb Package (Optional)

```bash
# Install FPM
sudo gem install --no-document fpm

# Build!
./build/build_deb.sh
```

**Output**: `spotlightx_1.1.0-1_amd64.deb` ✅

---

## ❓ FAQ (Frequently Asked Questions)

### Q: Why don't my applications show up?

**A:** Wait a few seconds for the first indexing. Or restart the app:
```bash
pkill -f spotlightx
spotlightx
```

### Q: Can't find my files?

**A:** SpotlightX searches in:
- ~/Documents
- ~/Downloads  
- ~/Desktop
- ~/Pictures
- ~/Videos
- ~/Music

Make sure your file is in one of these folders.

### Q: How much memory does it use?

**A:** Very lightweight! Only 30-120 MB (depending on the number of indexed files).

### Q: Is it safe?

**A:** 100% safe!
- ✅ Open source
- ✅ No root required
- ✅ No data sent to the internet
- ✅ No ads/tracking

### Q: Which distros can I use it on?

**A:** All Debian/Ubuntu-based distros:
- Ubuntu (20.04+)
- Debian (11+)
- Linux Mint
- Pop!_OS
- Elementary OS
- Zorin OS
- And more!

---

## 📚 Complete Documentation

Need more detailed info? See:

- [README.md](README.md) - Complete overview
- [USER_GUIDE.md](docs/USER_GUIDE.md) - Detailed user guide
- [PLUGIN_DEV_GUIDE.md](docs/PLUGIN_DEV_GUIDE.md) - Create custom plugins
- [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) - Build & packaging
- [RUNNING_FROM_SOURCE.md](docs/RUNNING_FROM_SOURCE.md) - Developer guide
- [CHANGELOG.md](CHANGELOG.md) - Change history

---

## 🐛 Having Problems?

1. **Restart the app**:
   ```bash
   pkill -f spotlightx && spotlightx
   ```

2. **Clear cache**:
   ```bash
   rm -rf ~/.cache/spotlightx/*
   spotlightx
   ```

3. **Still having errors?** [Report here](https://github.com/WHO-AM-I-404/spotlightx/issues)

---

## 🎓 Video Tutorial (Coming Soon)

Coming soon! Step-by-step video tutorials will be available soon.

---

## 💝 Support the Project

Like SpotlightX? Help us:

- ⭐ Star on GitHub
- 🐛 Report bugs
- 💡 Suggest features  
- 🔌 Create plugins
- 📢 Share with friends!

---

## 📞 Contact

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/WHO-AM-I-404/spotlightx/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/WHO-AM-I-404/spotlightx/discussions)
- 📧 **Email**: WHO-AM-I-404

---

**Enjoy using SpotlightX! May your productivity soar! 🚀**

**Copyright (c) 2025 WHO-AM-I-404 | Licensed under the MIT License**
