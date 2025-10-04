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
Search engine module for SpotlightX.
Implements fuzzy matching with rapidfuzz and ranking algorithm.
"""

import re
import math
from typing import List, Dict, Any, Optional
from rapidfuzz import fuzz, process
from .utils import get_file_type, format_file_size


class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer
        
        self.weights = {
            'exact_match': 30,
            'fuzzy_ratio': 0.6,
            'recent_boost': 0.4,
            'type_app': 10,
            'type_file': 5,
            'type_web': 2,
            'type_calc': 50
        }
    
    def is_calculator_query(self, query: str) -> bool:
        """Check if query is a calculator expression."""
        calc_pattern = r'^[\d\s\+\-\*\/\(\)\.\%]+$'
        return bool(re.match(calc_pattern, query.strip()))
    
    def evaluate_calculator(self, query: str) -> Optional[Dict[str, Any]]:
        """Safely evaluate calculator expression."""
        try:
            allowed_chars = set('0123456789+-*/().% ')
            if not all(c in allowed_chars for c in query):
                return None
            
            query = query.replace('%', '/100')
            
            result = eval(query, {"__builtins__": {}}, {})
            
            return {
                'type': 'calc',
                'name': f"{query} = {result}",
                'subtitle': 'Calculator',
                'action': str(result),
                'icon': 'calc',
                'score': 1000
            }
        except Exception:
            return None
    
    def is_url_query(self, query: str) -> bool:
        """Check if query looks like a URL."""
        url_pattern = r'^(https?://|www\.|[a-zA-Z0-9-]+\.(com|org|net|io|dev|co))'
        return bool(re.match(url_pattern, query.strip(), re.IGNORECASE))
    
    def create_url_result(self, query: str) -> Dict[str, Any]:
        """Create result for opening URL."""
        url = query.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return {
            'type': 'url',
            'name': url,
            'subtitle': 'Open in browser',
            'action': url,
            'icon': 'web',
            'score': 900
        }
    
    def parse_web_shortcut(self, query: str) -> Optional[Dict[str, Any]]:
        """Parse web search shortcuts like 'g query', 'yt query', etc."""
        shortcuts = {
            'g ': ('Google', 'https://www.google.com/search?q='),
            'yt ': ('YouTube', 'https://www.youtube.com/results?search_query='),
            'ddg ': ('DuckDuckGo', 'https://duckduckgo.com/?q='),
            'gh ': ('GitHub', 'https://github.com/search?q='),
            'so ': ('Stack Overflow', 'https://stackoverflow.com/search?q='),
            'wiki ': ('Wikipedia', 'https://en.wikipedia.org/wiki/Special:Search?search='),
        }
        
        for prefix, (name, url_template) in shortcuts.items():
            if query.lower().startswith(prefix):
                search_term = query[len(prefix):].strip()
                if search_term:
                    url = url_template + search_term.replace(' ', '+')
                    return {
                        'type': 'web',
                        'name': f"Search {name} for '{search_term}'",
                        'subtitle': name,
                        'action': url,
                        'icon': 'web',
                        'score': 850
                    }
        
        return None
    
    def calculate_score(self, item: Dict[str, Any], query: str) -> float:
        """Calculate relevance score for an item."""
        score = 0.0
        
        item_name = item.get('name', '').lower()
        query_lower = query.lower()
        
        if query_lower == item_name:
            score += self.weights['exact_match']
        
        fuzzy_score = fuzz.ratio(query_lower, item_name)
        score += fuzzy_score * self.weights['fuzzy_ratio']
        
        usage_data = self.indexer.get_usage(item.get('path', item.get('name', '')))
        usage_count = usage_data.get('count', 0)
        if usage_count > 0:
            score += self.weights['recent_boost'] * math.log(usage_count + 1)
        
        item_type = item.get('type', '')
        if item_type == 'app':
            score += self.weights['type_app']
        elif item_type == 'file':
            score += self.weights['type_file']
        elif item_type == 'web':
            score += self.weights['type_web']
        elif item_type == 'calc':
            score += self.weights['type_calc']
        
        return score
    
    def search(self, query: str, max_results: int = 12) -> List[Dict[str, Any]]:
        """
        Search for items matching the query.
        Returns sorted list of results.
        """
        if not query or not query.strip():
            return []
        
        query = query.strip()
        results = []
        
        calc_result = self.evaluate_calculator(query)
        if calc_result:
            return [calc_result]
        
        if self.is_url_query(query):
            results.append(self.create_url_result(query))
        
        web_shortcut = self.parse_web_shortcut(query)
        if web_shortcut:
            results.append(web_shortcut)
        
        apps = self.indexer.get_apps()
        for app in apps:
            app_copy = app.copy()
            app_copy['score'] = self.calculate_score(app, query)
            app_copy['subtitle'] = app.get('comment', 'Application')
            app_copy['action'] = app.get('exec', '')
            
            if app_copy['score'] > 30:
                results.append(app_copy)
        
        files = self.indexer.get_files()
        for file_item in files:
            file_copy = file_item.copy()
            file_copy['score'] = self.calculate_score(file_item, query)
            
            filepath = file_item.get('path', '')
            file_type = get_file_type(filepath)
            file_size = format_file_size(file_item.get('size', 0))
            
            file_copy['subtitle'] = f"{file_type} — {file_size} — {filepath}"
            file_copy['action'] = filepath
            
            if file_copy['score'] > 20:
                results.append(file_copy)
        
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return results[:max_results]
