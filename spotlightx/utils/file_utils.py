#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SpotlightX - Sophisticated Linux Application Launcher
# Copyright (c) 2025 WHO-AM-I-404
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
File utilities for SpotlightX
Enhanced file searching capabilities
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional


def find_files_by_pattern(pattern: str, search_paths: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Find files matching a pattern across search paths.
    
    Args:
        pattern: File pattern to search (e.g., "*.pdf", "report*")
        search_paths: List of paths to search (default: common user dirs)
    
    Returns:
        List of matching file dicts
    """
    if search_paths is None:
        search_paths = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Videos"),
            os.path.expanduser("~/Music"),
        ]
    
    results = []
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
        
        try:
            path = Path(search_path)
            
            if '*' in pattern or '?' in pattern:
                matches = path.rglob(pattern)
            else:
                matches = path.rglob(f"*{pattern}*")
            
            for match in matches:
                if match.is_file():
                    try:
                        stat = match.stat()
                        results.append({
                            'type': 'file',
                            'name': match.name,
                            'path': str(match),
                            'mtime': stat.st_mtime,
                            'size': stat.st_size
                        })
                    except Exception:
                        continue
        except Exception:
            continue
    
    return results


def get_file_type(filepath: str) -> str:
    """Get human-readable file type."""
    ext = os.path.splitext(filepath)[1].lower()
    
    type_map = {
        '.pdf': 'PDF Document',
        '.doc': 'Word Document',
        '.docx': 'Word Document',
        '.txt': 'Text File',
        '.py': 'Python Script',
        '.js': 'JavaScript File',
        '.html': 'HTML File',
        '.css': 'CSS File',
        '.jpg': 'JPEG Image',
        '.jpeg': 'JPEG Image',
        '.png': 'PNG Image',
        '.gif': 'GIF Image',
        '.mp3': 'MP3 Audio',
        '.mp4': 'MP4 Video',
        '.zip': 'ZIP Archive',
        '.tar': 'TAR Archive',
        '.gz': 'GZIP Archive',
    }
    
    return type_map.get(ext, 'File')


def format_file_size(size_bytes: int) -> str:
    """Format file size to human-readable string."""
    size: float = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"
