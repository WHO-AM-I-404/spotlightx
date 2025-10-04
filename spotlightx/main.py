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
Main entry point for SpotlightX.
"""

import sys
import signal
from spotlightx.indexer import Indexer
from spotlightx.search import SearchEngine
from spotlightx.executor import Executor
from spotlightx.plugin_manager import PluginManager
from spotlightx.ui import TkinterUI


class SpotlightX:
    def __init__(self):
        print("Initializing SpotlightX...")
        
        self.indexer = Indexer()
        self.search_engine = SearchEngine(self.indexer)
        self.executor = Executor()
        self.plugin_manager = PluginManager()
        
        print("Loading plugins...")
        self.plugin_manager.load_all_plugins()
        self.plugin_manager.trigger_hook('on_startup')
        
        print("Starting initial indexing...")
        self.indexer.index_all_async()
        
        self.ui = TkinterUI(
            on_query_callback=self.handle_query,
            on_select_callback=self.handle_select
        )
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def handle_query(self, query: str):
        """Handle search query."""
        plugin_results = self.plugin_manager.trigger_hook('on_query', query)
        
        search_results = self.search_engine.search(query)
        
        for plugin_result in plugin_results:
            if isinstance(plugin_result, list):
                search_results.extend(plugin_result)
        
        return search_results
    
    def handle_select(self, item: dict):
        """Handle item selection."""
        self.plugin_manager.trigger_hook('on_open', item)
        
        success = self.executor.execute(item)
        
        if success:
            item_id = item.get('path', item.get('name', ''))
            self.indexer.record_usage(item_id)
    
    def signal_handler(self, sig, frame):
        """Handle shutdown signals."""
        print("\nShutting down SpotlightX...")
        self.plugin_manager.trigger_hook('on_shutdown')
        sys.exit(0)
    
    def run(self):
        """Run the application."""
        print("SpotlightX is ready!")
        print("Press Ctrl+C to quit, or click the window to start searching")
        self.ui.show()
        self.ui.run()


def main():
    """Main entry point."""
    app = SpotlightX()
    app.run()


if __name__ == '__main__':
    main()
