import psutil
import os
import time
import threading
from typing import Set
import subprocess
import sys
import objc
from Foundation import (
    NSWorkspace, 
    NSBundle, 
    NSDictionary
)
from AppKit import NSRunningApplication
from ApplicationServices import AXIsProcessTrusted, AXIsProcessTrustedWithOptions, kAXTrustedCheckOptionPrompt
from PyQt6.QtWidgets import QMessageBox

class BlockingManager:
    def __init__(self):
        self.blocked_apps: Set[str] = set()
        self.is_active = False
        self.downtime_mode = False
        self.monitor_thread = None
        self.has_permissions = False
        
        if sys.platform == "darwin":
            self.setup_macos_permissions()
        
        # Load private frameworks
        self.workspace = NSWorkspace.sharedWorkspace()
        self.load_private_frameworks()
    
    def setup_macos_permissions(self):
        """Setup and check macOS permissions"""
        try:
            # Import required frameworks
            from ApplicationServices import AXIsProcessTrusted, AXIsProcessTrustedWithOptions
            from Foundation import NSDictionary
            
            # Check if we have permissions
            trusted = AXIsProcessTrusted()
            if not trusted:
                # This will trigger the system permission prompt
                options = NSDictionary.dictionaryWithObject_forKey_(False, "AXTrustedCheckOptionPrompt")
                AXIsProcessTrustedWithOptions(options)
                
                # Show our custom guidance
                self.show_permission_guidance()
                return False
            
            self.has_permissions = True
            return True
            
        except Exception as e:
            print(f"Error checking permissions: {e}")
            return False
    
    def show_permission_guidance(self):
        """Show guidance for enabling permissions"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Permission Required")
        msg.setText("BuildBlock needs permission to manage other applications")
        msg.setInformativeText(
            "macOS will now ask for Accessibility permissions.\n\n"
            "Please click 'Open System Settings' in the prompt\n"
            "and enable BuildBlock in the list."
        )
        msg.exec()
    
    def add_app(self, app_path: str):
        """Add an application to block list"""
        try:
            # Verify it's a valid app bundle
            bundle = NSBundle.bundleWithPath_(app_path)
            if bundle:
                self.blocked_apps.add(app_path)
                print(f"Successfully added {app_path} to block list")  # Debug print
                print(f"Current blocked apps: {self.blocked_apps}")  # Debug print
                return True
            print(f"Failed to add {app_path} - not a valid bundle")  # Debug print
            return False
        except Exception as e:
            print(f"Error adding app: {e}")
            return False
    
    def toggle_blocking(self, state: bool):
        """Toggle the blocking state"""
        print(f"Toggling blocking to {state}")  # Debug print
        if state and not self.has_permissions:
            print("No permissions, requesting...")  # Debug print
            self.setup_macos_permissions()
            return False
        
        self.is_active = state
        if state:
            print("Starting blocking thread...")  # Debug print
            self.start_blocking()
        else:
            print("Stopping blocking...")  # Debug print
            self.stop_blocking()
        return True
    
    def _monitor_processes(self):
        """Monitor and terminate blocked processes"""
        print(f"Starting monitor with blocked apps: {self.blocked_apps}")
        
        while self.is_active:
            try:
                workspace = NSWorkspace.sharedWorkspace()
                running_apps = workspace.runningApplications()
                
                for app in running_apps:
                    try:
                        if not app.bundleURL():
                            continue
                            
                        app_path = app.bundleURL().path()
                        if app_path in self.blocked_apps:
                            print(f"Blocking {app_path}")
                            
                            # Use Apple Events to quit the app
                            bundle_id = app.bundleIdentifier()
                            if bundle_id:
                                script = f'''
                                    tell application "System Events"
                                        tell application "{bundle_id}"
                                            quit
                                        end tell
                                    end tell
                                '''
                                os.system(f"osascript -e '{script}'")
                                print(f"Sent quit command to {bundle_id}")
                                
                    except Exception as e:
                        print(f"Error handling app: {e}")
                        
            except Exception as e:
                print(f"Monitor error: {e}")
            time.sleep(1) 
    
    def remove_app(self, app_path: str):
        """Remove an application from block list"""
        self.blocked_apps.discard(app_path)
        print(f"Removed {app_path} from block list")
    
    def set_downtime_mode(self, enabled: bool):
        """Set downtime mode"""
        self.downtime_mode = enabled
        if enabled and not self.is_active:
            self.start_blocking()
    
    def start_blocking(self):
        """Start the blocking monitor thread"""
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            print("Starting blocking thread")
            self.monitor_thread = threading.Thread(target=self._monitor_processes, daemon=True)
            self.monitor_thread.start()
    
    def stop_blocking(self):
        """Stop the blocking monitor thread"""
        print("Stopping blocking")
        self.is_active = False 
    
    def load_private_frameworks(self):
        """Load required private frameworks"""
        try:
            # Load Apple's private frameworks
            objc.loadBundle('CoreServices',
                          bundle_path='/System/Library/Frameworks/CoreServices.framework',
                          module_globals=globals())
                          
            objc.loadBundle('ApplicationServices',
                          bundle_path='/System/Library/Frameworks/ApplicationServices.framework',
                          module_globals=globals())
        except Exception as e:
            print(f"Failed to load frameworks: {e}")

    def check_permissions(self):
        """Check and request permissions properly"""
        try:
            # Check if we have accessibility permissions
            trusted = AXIsProcessTrusted()
            if not trusted:
                # Request permissions through official API
                options = {kAXTrustedCheckOptionPrompt: True}
                AXIsProcessTrustedWithOptions(options)
                return False
            return True
        except Exception as e:
            print(f"Permission check failed: {e}")
            return False

    def block_app(self, bundle_id):
        """Block an app using official APIs"""
        try:
            # Use private API to control app
            running_apps = self.workspace.runningApplications()
            for app in running_apps:
                if app.bundleIdentifier() == bundle_id:
                    # Use proper termination API
                    app.terminate()
                    return True
            return False
        except Exception as e:
            print(f"Failed to block app: {e}")
            return False 