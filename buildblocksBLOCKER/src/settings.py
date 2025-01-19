import json
import os
from typing import Dict, Optional
import base64

class Settings:
    def __init__(self):
        self.settings_dir = os.path.expanduser("~/Library/Application Support/AppBlocker")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self.ensure_settings_dir()
        
    def ensure_settings_dir(self):
        if not os.path.exists(self.settings_dir):
            os.makedirs(self.settings_dir)
    
    def save_settings(self, settings_dict: Dict) -> None:
        """Save all settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(settings_dict, f, indent=2)
    
    def load_settings(self) -> Dict:
        """Load all settings from file"""
        if not os.path.exists(self.settings_file):
            return {
                "blocked_apps": {},
                "salt": None,
                "downtime_enabled": False
            }
        
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {
                "blocked_apps": {},
                "salt": None,
                "downtime_enabled": False
            }
    
    def save_blocked_apps(self, app_paths: Dict[str, str]) -> None:
        """Save blocked apps to settings file"""
        settings = self.load_settings()
        settings["blocked_apps"] = app_paths
        self.save_settings(settings)
    
    def load_blocked_apps(self) -> Dict[str, str]:
        """Load blocked apps from settings file"""
        settings = self.load_settings()
        return settings.get("blocked_apps", {})
    
    def save_password_salt(self, salt: bytes) -> None:
        """Save password salt"""
        settings = self.load_settings()
        settings["salt"] = base64.b64encode(salt).decode('utf-8')
        self.save_settings(settings)
    
    def get_password_salt(self) -> Optional[bytes]:
        """Get stored password salt"""
        settings = self.load_settings()
        salt = settings.get("salt")
        return base64.b64decode(salt.encode('utf-8')) if salt else None
    
    def has_password(self) -> bool:
        """Check if a password has been set"""
        return self.get_password_salt() is not None
    
    def save_state(self, blocking_enabled: bool, downtime_enabled: bool) -> None:
        """Save the current state of blocking and downtime"""
        settings = self.load_settings()
        settings["last_state"] = {
            "blocking_enabled": blocking_enabled,
            "downtime_enabled": downtime_enabled
        }
        self.save_settings(settings) 
    
    def get_tutorial_shown(self) -> bool:
        """Check if tutorial has been shown"""
        settings = self.load_settings()
        return settings.get("tutorial_shown", False)
    
    def set_tutorial_shown(self, shown: bool):
        """Set tutorial shown state"""
        settings = self.load_settings()
        settings["tutorial_shown"] = shown
        self.save_settings(settings) 
    
    def clear_settings(self):
        """Clear all settings and start fresh"""
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        
        # Reset to defaults
        return {
            "blocked_apps": {},
            "salt": None,
            "downtime_enabled": False
        }
    
    def reset_password(self):
        """Remove just the password salt"""
        settings = self.load_settings()
        settings["salt"] = None
        self.save_settings(settings) 