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
Safe executor module for SpotlightX.
Launches applications and files without shell injection vulnerabilities.
"""

import os
import re
import subprocess
import shlex
from typing import Optional


class Executor:
    def __init__(self):
        pass
    
    def parse_desktop_exec(self, exec_str: str) -> list:
        """
        Parse .desktop Exec field safely, removing field codes.
        Field codes: %f, %F, %u, %U, %c, %k, %i, %d, %D, %n, %N, %m, %v
        """
        exec_str = re.sub(r'%[fFuUckidDnNmv]', '', exec_str)
        
        try:
            parts = shlex.split(exec_str)
            return parts
        except Exception:
            return [exec_str]
    
    def execute_app(self, exec_str: str) -> bool:
        """Execute an application from .desktop Exec field."""
        try:
            args = self.parse_desktop_exec(exec_str)
            
            if not args:
                return False
            
            subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception as e:
            print(f"Error executing app: {e}")
            return False
    
    def execute_file(self, filepath: str) -> bool:
        """Open a file with xdg-open."""
        try:
            subprocess.Popen(
                ['xdg-open', filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception as e:
            print(f"Error opening file: {e}")
            return False
    
    def execute_url(self, url: str) -> bool:
        """Open a URL with xdg-open."""
        try:
            subprocess.Popen(
                ['xdg-open', url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception as e:
            print(f"Error opening URL: {e}")
            return False
    
    def execute(self, item: dict) -> bool:
        """Execute an item based on its type."""
        item_type = item.get('type', '')
        action = item.get('action', '')
        
        if not action:
            return False
        
        if item_type == 'app':
            return self.execute_app(action)
        elif item_type == 'file':
            return self.execute_file(action)
        elif item_type in ('url', 'web'):
            return self.execute_url(action)
        elif item_type == 'calc':
            try:
                import pyperclip
                pyperclip.copy(action)
                print(f"Result copied to clipboard: {action}")
                return True
            except Exception:
                print(f"Calculator result: {action}")
                return True
        
        return False
