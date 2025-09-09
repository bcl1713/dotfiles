#!/usr/bin/env python3
"""
Syncthing Event Monitor for Waybar
Monitors Syncthing events via REST API and generates status JSON file
"""

import json
import requests
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class SyncthingMonitor:
    def __init__(self, api_url: str = "http://localhost:8384", api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.status_file = "/tmp/syncthing_status.json"
        self.last_event_id = 0
        self.current_status = {
            "text": "Syncthing",
            "tooltip": "Syncthing status unknown",
            "class": "unknown"
        }
        self.folder_states = {}
        self.device_states = {}
        self.sync_errors = []
        
    def get_api_key(self) -> Optional[str]:
        """Try to read API key from Syncthing config"""
        config_paths = [
            os.path.expanduser("~/.local/state/syncthing/config.xml"),
            os.path.expanduser("~/.config/syncthing/config.xml"),
            os.path.expanduser("~/.local/share/syncthing/config.xml"),
            "/etc/syncthing/config.xml"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        content = f.read()
                        # Simple extraction of API key
                        if '<apikey>' in content and '</apikey>' in content:
                            start = content.find('<apikey>') + 8
                            end = content.find('</apikey>')
                            return content[start:end]
                except Exception:
                    continue
        return None
    
    def make_request(self, endpoint: str, params: Dict = None) -> Optional[Any]:
        """Make authenticated request to Syncthing API"""
        if not self.api_key:
            self.api_key = self.get_api_key()
        
        if not self.api_key:
            print("Error: No API key found. Please configure Syncthing API key.")
            return None
        
        headers = {'X-API-Key': self.api_key}
        url = f"{self.api_url}/rest{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=65)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_folder_status(self) -> Dict[str, str]:
        """Get current folder statuses - not needed, we get this from events"""
        return {}
    
    def get_device_status(self) -> Dict[str, bool]:
        """Get current device connection statuses"""
        connections = self.make_request("/system/connections")
        if not connections or 'connections' not in connections:
            return {}
        
        statuses = {}
        for device_id, conn in connections['connections'].items():
            statuses[device_id] = conn.get('connected', False)
        
        return statuses
    
    def process_event(self, event: Dict[str, Any]):
        """Process a single Syncthing event"""
        event_type = event.get('type')
        event_data = event.get('data', {})
        
        if event_type in ['FolderCompletion', 'FolderScanProgress', 'FolderErrors']:
            folder_id = event_data.get('folder')
            if folder_id:
                if event_type == 'FolderCompletion':
                    completion = event_data.get('completion', 0)
                    self.folder_states[folder_id] = {
                        'completion': completion,
                        'state': 'syncing' if completion < 100 else 'idle'
                    }
                elif event_type == 'FolderErrors':
                    errors = event_data.get('errors', [])
                    if errors:
                        self.sync_errors.extend(errors)
                        self.sync_errors = self.sync_errors[-10:]  # Keep last 10 errors
        
        elif event_type in ['DeviceConnected', 'DeviceDisconnected']:
            device_id = event_data.get('id')
            if device_id:
                self.device_states[device_id] = event_type == 'DeviceConnected'
        
        elif event_type in ['LocalChangeDetected', 'RemoteChangeDetected']:
            folder_id = event_data.get('folderID')
            if folder_id:
                self.folder_states[folder_id] = {'state': 'syncing'}
    
    def update_status(self):
        """Update the current status based on folder and device states"""
        # Count syncing folders
        syncing_folders = sum(1 for state in self.folder_states.values() 
                            if isinstance(state, dict) and state.get('state') == 'syncing')
        
        # Count connected devices
        connected_devices = sum(1 for connected in self.device_states.values() if connected)
        total_devices = len(self.device_states)
        
        # Determine overall status
        if self.sync_errors:
            status_class = "error"
            text = f"{len(self.sync_errors)} errors ⚠"
        elif syncing_folders > 0:
            status_class = "syncing"
            text = f"{syncing_folders} syncing ↕"
        elif connected_devices == 0 and total_devices > 0:
            status_class = "disconnected"
            text = "Disconnected ⚪"
        elif connected_devices < total_devices:
            status_class = "partial"
            text = f"{connected_devices}/{total_devices} devices 🔶"
        else:
            status_class = "idle"
            text = "Synced ✓"
        
        # Build tooltip
        tooltip_parts = []
        
        if self.sync_errors:
            tooltip_parts.append(f"Errors: {len(self.sync_errors)}")
            tooltip_parts.extend(self.sync_errors[-3:])  # Show last 3 errors
        
        if syncing_folders > 0:
            tooltip_parts.append(f"Syncing folders: {syncing_folders}")
        
        if self.device_states:
            tooltip_parts.append(f"Devices: {connected_devices}/{total_devices} connected")
        
        tooltip_parts.append(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
        self.current_status = {
            "text": text,
            "tooltip": "\n".join(tooltip_parts),
            "class": status_class
        }
    
    def write_status_file(self):
        """Write current status to JSON file atomically"""
        try:
            temp_file = self.status_file + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump(self.current_status, f, ensure_ascii=False, separators=(',', ':'))
                f.write('\n')  # Add newline at end
            os.rename(temp_file, self.status_file)
        except Exception as e:
            print(f"Error writing status file: {e}")
    
    def run(self):
        """Main monitoring loop"""
        print(f"Starting Syncthing monitor, writing status to {self.status_file}")
        
        # Initial status check
        self.folder_states = self.get_folder_status()
        self.device_states = self.get_device_status()
        self.update_status()
        self.write_status_file()
        
        while True:
            try:
                # Poll for events
                events = self.make_request("/events", {
                    'since': self.last_event_id,
                    'timeout': 60
                })
                
                if events is None:
                    time.sleep(5)
                    continue
                
                # Process events
                for event in events:
                    self.process_event(event)
                    self.last_event_id = max(self.last_event_id, event.get('id', 0))
                
                # Update status if we got events
                if events:
                    self.update_status()
                    self.write_status_file()
                
            except KeyboardInterrupt:
                print("\nShutting down monitor...")
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(5)

def main():
    """Main entry point"""
    monitor = SyncthingMonitor()
    monitor.run()

if __name__ == "__main__":
    main()