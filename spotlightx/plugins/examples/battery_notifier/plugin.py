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
Battery Notifier Plugin for SpotlightX
Shows battery status in search results.
"""

import os


class BatteryNotifier:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
    
    def get_battery_status(self):
        """Get battery status from /sys/class/power_supply."""
        try:
            battery_path = "/sys/class/power_supply/BAT0"
            
            if not os.path.exists(battery_path):
                battery_path = "/sys/class/power_supply/BAT1"
            
            if not os.path.exists(battery_path):
                return None
            
            with open(f"{battery_path}/capacity", 'r') as f:
                capacity = int(f.read().strip())
            
            with open(f"{battery_path}/status", 'r') as f:
                status = f.read().strip()
            
            return {'capacity': capacity, 'status': status}
        except Exception:
            return None
    
    def on_query(self, query: str):
        """Show battery status when queried."""
        if query.lower() not in ['battery', 'bat', 'power']:
            return None
        
        status = self.get_battery_status()
        
        if not status:
            return [{
                'type': 'info',
                'name': 'Battery status unavailable',
                'subtitle': 'No battery detected',
                'action': '',
                'icon': 'battery',
                'score': 900
            }]
        
        capacity = status['capacity']
        charging_status = status['status']
        
        return [{
            'type': 'info',
            'name': f"Battery: {capacity}% ({charging_status})",
            'subtitle': f"Status: {charging_status}",
            'action': '',
            'icon': 'battery',
            'score': 900
        }]


def register(plugin_manager):
    """Register the plugin."""
    battery = BatteryNotifier(plugin_manager)
    plugin_manager.register_hook('on_query', battery.on_query)
