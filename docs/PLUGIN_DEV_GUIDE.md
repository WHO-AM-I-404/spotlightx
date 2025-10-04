# SpotlightX Plugin Development Guide

Complete guide to creating custom plugins for SpotlightX.

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Plugin Structure](#plugin-structure)
3. [Plugin API](#plugin-api)
4. [Hooks](#hooks)
5. [Examples](#examples)
6. [Best Practices](#best-practices)
7. [Distribution](#distribution)

## Introduction

Plugin system SpotlightX memungkinkan Anda extend functionality tanpa modify core code. Plugin dapat:

- Add custom search results
- React to user actions
- Run background tasks
- Store persistent data
- Integrate external services

### Plugin Architecture

- **Sandboxed execution** - Plugins run dalam process yang sama namun isolated
- **Hook-based** - Plugins register callbacks untuk specific events
- **Config management** - Built-in config storage per plugin
- **Opt-in** - Users harus explicitly enable plugins

## Plugin Structure

Setiap plugin adalah folder dengan minimal 2 files:

```
my_plugin/
├── plugin.json          # Metadata & configuration
└── plugin.py            # Implementation code
```

### Directory Layout

```bash
~/.config/spotlightx/plugins/
└── my_plugin/
    ├── plugin.json      # Required: Plugin metadata
    ├── plugin.py        # Required: Plugin code
    ├── config.json      # Optional: User config
    ├── README.md        # Optional: Documentation
    └── assets/          # Optional: Images, data files
        └── icon.png
```

## Plugin API

### plugin.json

File metadata yang mendefinisikan plugin:

```json
{
  "id": "my_plugin",
  "name": "My Awesome Plugin",
  "version": "1.0.0",
  "description": "A plugin that does awesome things",
  "author": "YOUR_NAME",
  "enabled": false,
  "requires": []
}
```

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (alphanumeric, underscore) |
| `name` | string | Yes | Display name |
| `version` | string | Yes | Semantic version (1.0.0) |
| `description` | string | Yes | Short description |
| `author` | string | Yes | Author name |
| `enabled` | boolean | Yes | Enable/disable plugin |
| `requires` | array | No | Dependencies (future) |

### plugin.py

File implementasi dengan function `register()`:

```python
"""
My Plugin - Description
"""

def register(plugin_manager):
    """
    Entry point called by SpotlightX.
    
    Args:
        plugin_manager: PluginManager instance
    """
    # Register hooks here
    pass
```

## Hooks

Hooks adalah callbacks yang dipanggil pada specific events.

### Available Hooks

#### 1. on_query

Dipanggil setiap kali user mengetik query.

**Signature**:
```python
def on_query(query: str) -> Optional[List[Dict[str, Any]]]:
    """
    Args:
        query: User search query
        
    Returns:
        List of search results or None
    """
    pass
```

**Result Format**:
```python
{
    'type': 'app',           # Type: app, file, url, web, calc, info, action
    'name': 'Item Name',     # Display name (bold)
    'subtitle': 'Details',   # Subtitle text (gray)
    'action': '/path/to/file',  # Action data
    'icon': 'icon_name',     # Icon identifier
    'score': 850             # Relevance score (higher = top)
}
```

**Example**:
```python
def on_query(query: str):
    if query.startswith('hello'):
        return [{
            'type': 'info',
            'name': 'Hello World!',
            'subtitle': 'Greeting from my plugin',
            'action': '',
            'icon': 'wave',
            'score': 900
        }]
    return None
```

#### 2. on_open

Dipanggil ketika user open/execute item.

**Signature**:
```python
def on_open(item: Dict[str, Any]) -> None:
    """
    Args:
        item: The selected item dict
    """
    pass
```

**Example**:
```python
def on_open(item):
    item_name = item.get('name', '')
    print(f"User opened: {item_name}")
    
    # Log to file, send analytics, etc.
```

#### 3. on_startup

Dipanggil saat plugin loaded.

**Signature**:
```python
def on_startup() -> None:
    """Called when plugin is initialized."""
    pass
```

**Example**:
```python
def on_startup():
    print("My plugin started!")
    # Initialize resources, start background threads, etc.
```

#### 4. on_shutdown

Dipanggil saat aplikasi closing.

**Signature**:
```python
def on_shutdown() -> None:
    """Called when application is shutting down."""
    pass
```

**Example**:
```python
def on_shutdown():
    # Cleanup, save state, close connections
    print("My plugin shutting down...")
```

### Registering Hooks

```python
def register(plugin_manager):
    # Register multiple hooks
    plugin_manager.register_hook('on_query', my_query_handler)
    plugin_manager.register_hook('on_open', my_open_handler)
    plugin_manager.register_hook('on_startup', my_startup_handler)
    plugin_manager.register_hook('on_shutdown', my_shutdown_handler)
```

## PluginManager API

The `plugin_manager` object provides utilities:

### get_plugin_config_dir()

Get plugin's config directory:

```python
def register(plugin_manager):
    config_dir = plugin_manager.get_plugin_config_dir('my_plugin')
    # Returns: Path('~/.config/spotlightx/plugins/my_plugin')
    
    # Use for storing data
    data_file = config_dir / 'data.json'
```

### get_plugin_config()

Load plugin configuration:

```python
config = plugin_manager.get_plugin_config('my_plugin')
# Returns: dict from config.json
```

### save_plugin_config()

Save plugin configuration:

```python
config = {
    'api_key': 'secret',
    'enabled_features': ['feature1', 'feature2']
}
plugin_manager.save_plugin_config('my_plugin', config)
```

## Examples

### Example 1: Simple Info Plugin

```python
"""
Info Plugin - Shows static information
"""

def on_query(query: str):
    if query.lower() == 'info':
        return [{
            'type': 'info',
            'name': 'SpotlightX v1.0.0',
            'subtitle': 'Lightweight launcher for Linux',
            'action': '',
            'icon': 'info',
            'score': 900
        }]
    return None

def register(plugin_manager):
    plugin_manager.register_hook('on_query', on_query)
```

### Example 2: Calculator Extension

```python
"""
Advanced Calculator - Extended math functions
"""

import math

def on_query(query: str):
    query = query.strip().lower()
    
    # Sin, cos, tan functions
    if query.startswith('sin('):
        try:
            value = float(query[4:-1])
            result = math.sin(math.radians(value))
            return [{
                'type': 'calc',
                'name': f'sin({value}°) = {result:.4f}',
                'subtitle': 'Trigonometry',
                'action': str(result),
                'icon': 'calc',
                'score': 1000
            }]
        except:
            pass
    
    return None

def register(plugin_manager):
    plugin_manager.register_hook('on_query', on_query)
```

### Example 3: API Integration

```python
"""
Weather Plugin - Shows weather from API
"""

import requests
import json
from datetime import datetime

class WeatherPlugin:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.config = self.pm.get_plugin_config('weather')
        self.api_key = self.config.get('api_key', '')
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes
    
    def get_weather(self, city):
        # Check cache
        now = datetime.now().timestamp()
        if city in self.cache:
            cached_time, cached_data = self.cache[city]
            if now - cached_time < self.cache_ttl:
                return cached_data
        
        # Fetch from API
        if not self.api_key:
            return None
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            # Cache result
            self.cache[city] = (now, data)
            return data
        except:
            return None
    
    def on_query(self, query: str):
        if not query.lower().startswith('weather '):
            return None
        
        city = query[8:].strip()
        if not city:
            return None
        
        weather = self.get_weather(city)
        if not weather:
            return [{
                'type': 'info',
                'name': 'Unable to fetch weather',
                'subtitle': 'Check API key in config',
                'action': '',
                'icon': 'weather',
                'score': 800
            }]
        
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        
        return [{
            'type': 'info',
            'name': f"{city.title()}: {temp}°C",
            'subtitle': description.title(),
            'action': '',
            'icon': 'weather',
            'score': 900
        }]

def register(plugin_manager):
    weather = WeatherPlugin(plugin_manager)
    plugin_manager.register_hook('on_query', weather.on_query)
```

config.json untuk weather plugin:
```json
{
  "api_key": "YOUR_OPENWEATHERMAP_API_KEY"
}
```

### Example 4: File Watcher

```python
"""
Project Watcher - Track recently modified project files
"""

import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectWatcher:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.recent_files = []
        self.max_files = 20
        
        # Watch ~/Projects directory
        self.watch_dir = Path.home() / 'Projects'
        
        if self.watch_dir.exists():
            event_handler = self.FileHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, str(self.watch_dir), recursive=True)
            self.observer.start()
    
    class FileHandler(FileSystemEventHandler):
        def __init__(self, watcher):
            self.watcher = watcher
        
        def on_modified(self, event):
            if not event.is_directory:
                self.watcher.add_recent_file(event.src_path)
    
    def add_recent_file(self, filepath):
        # Remove if exists
        self.recent_files = [f for f in self.recent_files if f['path'] != filepath]
        
        # Add to top
        self.recent_files.insert(0, {
            'path': filepath,
            'name': os.path.basename(filepath),
            'time': time.time()
        })
        
        # Limit size
        self.recent_files = self.recent_files[:self.max_files]
    
    def on_query(self, query: str):
        if query.lower() not in ['recent', 'projects']:
            return None
        
        results = []
        for file_info in self.recent_files[:10]:
            time_ago = int((time.time() - file_info['time']) / 60)
            results.append({
                'type': 'file',
                'name': file_info['name'],
                'subtitle': f"{file_info['path']} — {time_ago}m ago",
                'action': file_info['path'],
                'icon': 'file',
                'score': 850
            })
        
        return results
    
    def on_shutdown(self):
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()

def register(plugin_manager):
    watcher = ProjectWatcher(plugin_manager)
    plugin_manager.register_hook('on_query', watcher.on_query)
    plugin_manager.register_hook('on_shutdown', watcher.on_shutdown)
```

## Best Practices

### 1. Performance

**DO**:
- Cache expensive operations
- Return `None` early if query tidak relevant
- Use timeouts untuk network requests
- Limit result count (max 10-15 items)

**DON'T**:
- Block main thread dengan slow operations
- Return terlalu banyak results
- Fetch API on every keystroke

### 2. Security

**DO**:
- Validate user input
- Use timeout untuk external requests
- Store API keys in config.json
- Handle exceptions gracefully

**DON'T**:
- Execute shell commands dengan user input
- Store credentials in code
- Trust external data tanpa validation

### 3. User Experience

**DO**:
- Provide clear, descriptive names
- Use meaningful subtitles
- Set appropriate score values
- Test dengan real users

**DON'T**:
- Return irrelevant results
- Use vague descriptions
- Interfere dengan core functionality

### 4. Code Quality

**DO**:
- Add docstrings
- Handle errors gracefully
- Follow Python conventions
- Keep code simple & readable

**DON'T**:
- Use global state carelessly
- Ignore exceptions
- Create memory leaks
- Over-engineer

## Distribution

### Packaging

Create distributable package:

```bash
my_plugin/
├── plugin.json
├── plugin.py
├── README.md           # Usage instructions
├── requirements.txt    # Python dependencies (if any)
└── LICENSE            # License file
```

### Installation Instructions

Provide users with:

```markdown
## Installation

1. Download plugin:
   ```bash
   git clone https://github.com/yourname/spotlightx-myplugin
   ```

2. Copy to plugins directory:
   ```bash
   cp -r spotlightx-myplugin ~/.config/spotlightx/plugins/my_plugin
   ```

3. Enable plugin:
   ```bash
   nano ~/.config/spotlightx/plugins/my_plugin/plugin.json
   # Set "enabled": true
   ```

4. Restart SpotlightX:
   ```bash
   pkill -f spotlightx && spotlightx
   ```

## Configuration

Edit `~/.config/spotlightx/plugins/my_plugin/config.json`:

```json
{
  "api_key": "YOUR_API_KEY",
  "option": "value"
}
```
```

### Sharing

Share your plugin:

1. **GitHub** - Host source code
2. **README** - Clear documentation
3. **Examples** - Usage examples
4. **Issues** - Support users

## Testing

### Manual Testing

```bash
# Enable plugin
nano ~/.config/spotlightx/plugins/my_plugin/plugin.json

# Run SpotlightX
spotlightx

# Test queries
# - Type expected queries
# - Verify results appear
# - Test actions execute correctly
```

### Debug Logging

Add debug prints:

```python
def on_query(query: str):
    print(f"[MY_PLUGIN] Query: {query}")
    # Your code here
    print(f"[MY_PLUGIN] Returning {len(results)} results")
    return results
```

View logs:
```bash
spotlightx 2>&1 | grep MY_PLUGIN
```

## FAQ

### Q: Can I use external Python libraries?

A: Yes, but users must install them. Include `requirements.txt`:

```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
```

Users install with:
```bash
pip install -r ~/.config/spotlightx/plugins/my_plugin/requirements.txt
```

### Q: Can plugins communicate with each other?

A: Not directly. Plugins are isolated. Use plugin_manager config storage for shared state jika diperlukan.

### Q: Performance impact?

A: Plugins dipanggil untuk setiap query. Optimize dengan:
- Early return jika query tidak relevant
- Caching
- Lazy loading
- Async operations (advanced)

### Q: Error handling?

A: Plugin errors tidak crash aplikasi. SpotlightX catches exceptions dan log errors.

### Q: Can I override core functionality?

A: No. Plugins extend, tidak replace core features.

---

**Questions?** [Open Issue](https://github.com/WHO-AM-I-404/spotlightx/issues) atau [Join Discussion](https://github.com/WHO-AM-I-404/spotlightx/discussions)
