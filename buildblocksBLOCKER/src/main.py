from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QListWidget, QLabel, QSystemTrayIcon, QFileDialog, 
                           QMenu, QMessageBox, QCheckBox, QFrame, QListWidgetItem)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from blocker import BlockingManager
import sys
import os
from typing import Dict
from settings import Settings
from password_dialog import PasswordDialog
from security import Security
from game_widgets import GameButton
from tutorial import Tutorial

class GameStyledFrame(QFrame):
    """A styled frame for grouping elements"""
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("HeaderSection")
        
        layout = QVBoxLayout(self)
        
        # Add header
        header = QLabel(title)
        header.setObjectName("GroupHeader")
        layout.addWidget(header)
        
        # Content widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        layout.addWidget(self.content)

class AppListItem(QListWidgetItem):
    def __init__(self, app_path: str, parent=None):
        super().__init__(parent)
        self.app_path = app_path
        self.app_name = os.path.basename(app_path)
        
        # Get the app's icon (macOS specific)
        icon = QIcon(app_path)
        self.setIcon(icon)
        self.setText(self.app_name)
        
        # Set size hint for better display
        self.setSizeHint(QSize(200, 40))

class AppBlocker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BuildBlock")
        self.setMinimumSize(1000, 700)
        
        # Initialize managers
        self.settings = Settings()
        self.blocking_manager = BlockingManager()
        self.security = Security()
        self.app_paths: Dict[str, str] = {}
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Control Section
        control_frame = GameStyledFrame("Control Panel")
        controls_layout = QHBoxLayout()
        
        # Left side controls
        left_controls = QVBoxLayout()
        self.block_toggle = GameButton("Enable BuildBlock", icon_type="guardian")
        self.block_toggle.setCheckable(True)
        self.block_toggle.clicked.connect(self.toggle_blocking)
        left_controls.addWidget(self.block_toggle)
        
        self.downtime_toggle = QCheckBox("Activate Full Lockdown")
        self.downtime_toggle.clicked.connect(self.toggle_downtime)
        left_controls.addWidget(self.downtime_toggle)
        
        controls_layout.addLayout(left_controls)
        
        # Right side controls
        right_controls = QVBoxLayout()
        self.add_button = GameButton("Add Application", icon_type="add")
        self.add_button.clicked.connect(self.browse_for_app)
        right_controls.addWidget(self.add_button)
        
        self.remove_button = GameButton("Remove Selected", icon_type="remove")
        self.remove_button.clicked.connect(self.remove_selected_app)
        right_controls.addWidget(self.remove_button)
        
        controls_layout.addLayout(right_controls)
        control_frame.content_layout.addLayout(controls_layout)
        layout.addWidget(control_frame)
        
        # Blocked Apps Section
        apps_frame = GameStyledFrame("Protected Applications")
        self.app_list = QListWidget()
        apps_frame.content_layout.addWidget(self.app_list)
        layout.addWidget(apps_frame)
        
        # Schedule Section
        schedule_frame = GameStyledFrame("Time Restrictions")
        schedule_button = GameButton("Manage Schedules", icon_type="time")
        schedule_button.clicked.connect(self.show_schedule_dialog)
        schedule_frame.content_layout.addWidget(schedule_button)
        layout.addWidget(schedule_frame)
        
        # Add development notice (two rows)
        dev_notice_layout = QVBoxLayout()

        dev_notice_1 = QLabel(
            "🚧 The blocking features don't work because i don't have an apple developer account/100$ 🚧"
        )
        dev_notice_2 = QLabel(
            "Truly am in love with this idea and want V1's community to help to build this out! 💪"
        )

        for notice in [dev_notice_1, dev_notice_2]:
            notice.setStyleSheet("""
                QLabel {
                    color: #C8AA6E;
                    background: #1E2328;
                    border: 1px solid #785A28;
                    border-radius: 4px;
                    padding: 8px;
                    font-style: italic;
                    font-size: 13px;
                }
            """)
            notice.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dev_notice_layout.addWidget(notice)

        dev_notice_layout.setSpacing(4)  # Space between the two notices
        layout.addLayout(dev_notice_layout)
        
        # Setup system tray
        self.setup_tray()
        self.setup_tray_menu()
        
        # Load saved apps and settings
        self.load_saved_apps()
        self.load_settings()
        if not self.settings.has_password():
            self.setup_initial_password()
        
        # Check if we have necessary permissions before enabling blocking
        if sys.platform == "darwin":
            self._check_macos_permissions()
    
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("BuildBlock")
        
        # Connect double click to show/hide window
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def setup_tray_menu(self):
        """Create the system tray menu"""
        menu = QMenu()
        
        # Toggle blocking action
        self.tray_toggle_action = QAction("Enable Blocking", self)
        self.tray_toggle_action.setCheckable(True)
        self.tray_toggle_action.triggered.connect(self.block_toggle.click)
        menu.addAction(self.tray_toggle_action)
        
        menu.addSeparator()
        
        # Show/Hide window action
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)
        
        # Add Reset Password option
        reset_action = QAction("Reset Password", self)
        reset_action.triggered.connect(self.reset_password)
        menu.addAction(reset_action)
        
        menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation (usually double-click)"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()
    
    def show_window(self):
        """Show and bring window to front"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def quit_application(self):
        """Clean shutdown of the application"""
        if self.block_toggle.isChecked():
            # Show warning if blocking is active
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "BuildBlock is currently active. Quitting will disable protection.\n\n"
                "Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                return
            
            # Disable blocking before quitting
            self.blocking_manager.toggle_blocking(False)
        
        # Save current state
        self.settings.save_state(
            blocking_enabled=self.block_toggle.isChecked(),
            downtime_enabled=self.downtime_toggle.isChecked()
        )
        
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close button"""
        if self.block_toggle.isChecked():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Do you want to quit BuildBlock?\n\n"
                "You can also minimize to tray to keep protection active.",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.quit_application()
            elif reply == QMessageBox.StandardButton.No:
                event.ignore()
                self.hide()  # Minimize to tray
            else:  # Cancel
                event.ignore()
        else:
            reply = QMessageBox.question(
                self,
                "Exit Options",
                "Would you like to:\n\n"
                "Yes - Quit BuildBlock\n"
                "No - Minimize to tray",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.quit_application()
            else:
                event.ignore()
                self.hide()  # Minimize to tray
    
    def load_saved_apps(self):
        """Load previously saved blocked apps"""
        saved_apps = self.settings.load_blocked_apps()
        for name, path in saved_apps.items():
            list_item = AppListItem(path)
            self.app_list.addItem(list_item)
            self.app_paths[list_item.app_name] = path
            self.blocking_manager.add_app(path)
    
    def browse_for_app(self):
        try:
            default_path = "/Applications" if sys.platform == "darwin" else "/"
            
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Application",
                default_path,
                "Applications (*.app);;All Files (*.*)" if sys.platform == "darwin" else "All Files (*.*)"
            )
            
            if file_path:
                # Create custom list item with icon
                list_item = AppListItem(file_path)
                self.app_list.addItem(list_item)
                self.app_paths[list_item.app_name] = file_path
                self.blocking_manager.add_app(file_path)
                self.settings.save_blocked_apps(self.app_paths)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add application: {str(e)}")
    
    def remove_selected_app(self):
        current_item = self.app_list.currentItem()
        if current_item and isinstance(current_item, AppListItem):
            app_path = current_item.app_path
            self.app_list.takeItem(self.app_list.row(current_item))
            self.blocking_manager.remove_app(app_path)
            del self.app_paths[current_item.app_name]
            self.settings.save_blocked_apps(self.app_paths)
            
    def toggle_blocking(self, checked):
        """Toggle application blocking with password protection"""
        if checked:  # Enabling blocking
            if not self.verify_password():
                self.block_toggle.setChecked(False)
                return
            
            # Try to enable blocking
            if not self.blocking_manager.toggle_blocking(True):
                self.block_toggle.setChecked(False)
                return
            
        else:  # Disabling blocking
            if self.block_toggle.isChecked():  # Was previously enabled
                if not self.verify_password():
                    self.block_toggle.setChecked(True)
                    return
            
            self.blocking_manager.toggle_blocking(False)
        
        text = "Disable BuildBlock" if checked else "Enable BuildBlock"
        self.block_toggle.setText(text)
        self.tray_toggle_action.setText(text)
        self.add_button.setEnabled(not checked)
        self.remove_button.setEnabled(not checked)
    
    def toggle_downtime(self, checked):
        """Toggle global downtime mode"""
        if checked and not self.verify_password():
            self.downtime_toggle.setChecked(False)
            return
            
        if not checked and self.downtime_toggle.isChecked():
            if not self.verify_password():
                self.downtime_toggle.setChecked(True)
                return
        
        # Update settings
        settings = self.settings.load_settings()
        settings["downtime_enabled"] = checked
        self.settings.save_settings(settings)
        
        # Update blocking manager
        self.blocking_manager.set_downtime_mode(checked)
    
    def setup_initial_password(self):
        """Set up the initial password"""
        while True:
            dialog = PasswordDialog(self, is_setup=True)
            if dialog.exec():
                password, confirm = dialog.get_confirmed_password()
                if password == confirm and password:
                    salt = self.security.set_password(password)
                    self.settings.save_password_salt(salt)
                    # Start tutorial after password setup
                    self.tutorial.start()
                    self.settings.set_tutorial_shown(True)
                    break
                else:
                    QMessageBox.warning(self, "Error", "Passwords do not match or are empty!")
            else:
                # User cancelled - can't proceed without password
                sys.exit(1)
    
    def verify_password(self) -> bool:
        """Verify password before allowing sensitive operations"""
        dialog = PasswordDialog(self)
        if dialog.exec():
            salt = self.settings.get_password_salt()
            if self.security.verify_password(dialog.get_password(), salt):
                return True
            QMessageBox.warning(self, "Error", "Incorrect password!")
        return False
    
    def load_settings(self):
        """Load settings from file"""
        settings = self.settings.load_settings()
        self.downtime_toggle.setChecked(settings["downtime_enabled"])
    
    def show_schedule_dialog(self):
        """Show the schedule management dialog"""
        dialog = ScheduleDialog(self)
        if dialog.exec():
            schedule = dialog.get_schedule()
            # Here you would handle the schedule data
            # For example:
            if schedule['apps'] is None:  # Block all apps
                print("Blocking all apps during scheduled time")
            else:
                print(f"Blocking selected apps: {schedule['apps']}")
            print(f"Schedule: {schedule['start_time']} to {schedule['end_time']}")
            print(f"Days: {', '.join(schedule['days'])}")
    
    def show_tutorial(self):
        """Show the tutorial again"""
        self.tutorial.start()
    
    def _check_macos_permissions(self):
        """Check and request necessary macOS permissions"""
        try:
            import Foundation
            workspace = Foundation.NSWorkspace.sharedWorkspace()
            running_apps = workspace.runningApplications()
            
            # Try to get info about running apps - this will fail without permissions
            for app in running_apps:
                _ = app.bundleIdentifier()
        except Exception:
            QMessageBox.warning(
                self,
                "Permissions Required",
                "BuildBlock needs additional permissions to function properly.\n\n"
                "Please grant Accessibility access in System Preferences:\n"
                "System Preferences > Security & Privacy > Privacy > Accessibility\n\n"
                "Add this application to the list and try again."
            )
    
    def reset_password(self):
        """Reset the application password"""
        # Verify current password first
        if not self.verify_password():
            return
        
        # Now set new password
        dialog = PasswordDialog(self, is_setup=True)
        if dialog.exec():
            password, confirm = dialog.get_confirmed_password()
            if password == confirm and password:
                salt = self.security.set_password(password)
                self.settings.save_password_salt(salt)
                QMessageBox.information(self, "Success", "Password has been reset successfully!")
            else:
                QMessageBox.warning(self, "Error", "Passwords do not match or are empty!")
    
    def factory_reset(self):
        """Reset app to factory settings"""
        reply = QMessageBox.question(
            self,
            "Factory Reset",
            "This will reset all settings including password and blocked apps.\n\n"
            "Are you sure you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear all settings
            self.settings.clear_settings()
            # Clear current state
            self.app_list.clear()
            self.app_paths.clear()
            self.blocking_manager.blocked_apps.clear()
            # Reset password
            self.setup_initial_password()
            QMessageBox.information(self, "Reset Complete", "Application has been reset to factory settings.")

def main():
    app = QApplication(sys.argv)
    window = AppBlocker()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 