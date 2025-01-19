from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout, 
                           QWidget, QGraphicsOpacityEffect, QHBoxLayout,
                           QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint
from typing import List, Tuple

class TutorialStep:
    def __init__(self, target: QWidget, text: str, position: str = "bottom"):
        self.target = target
        self.text = text
        self.position = position

class TutorialPopup(QDialog):
    def __init__(self, text: str, parent=None):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main container with background
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: #1E2328;
                border: 2px solid #785A28;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout(container)
        
        # Scroll area for message
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #1E2328;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #785A28;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Message container
        message_container = QWidget()
        message_layout = QVBoxLayout(message_container)
        
        # Message
        message = QLabel(text)
        message.setStyleSheet("""
            QLabel {
                color: #C8AA6E;
                font-size: 14px;
                padding: 20px;
                background: transparent;
            }
        """)
        message.setWordWrap(True)
        message_layout.addWidget(message)
        
        scroll_area.setWidget(message_container)
        container_layout.addWidget(scroll_area)
        
        # Buttons container
        buttons_layout = QHBoxLayout()
        
        # Skip button (left-aligned)
        self.skip_button = QPushButton("Skip Tutorial")
        self.skip_button.clicked.connect(self.reject)
        self.skip_button.setStyleSheet(self._get_button_style("skip"))
        buttons_layout.addWidget(self.skip_button)
        
        buttons_layout.addStretch()
        
        # Next button (right-aligned)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.accept)
        self.next_button.setStyleSheet(self._get_button_style("next"))
        buttons_layout.addWidget(self.next_button)
        
        container_layout.addLayout(buttons_layout)
        layout.addWidget(container)
        
        # Set fixed width but allow height to adjust
        self.setFixedWidth(500)  # Made wider
        self.setMaximumHeight(400)  # Added max height
    
    def setFinalStep(self, is_final: bool):
        """Update button text for final step"""
        if is_final:
            self.next_button.setText("Get Started!")
            self.skip_button.hide()
    
    def _get_button_style(self, button_type: str) -> str:
        """Get button style based on type"""
        if button_type == "next":
            return """
                QPushButton {
                    background: #005A82;
                    color: #0AC8B9;
                    border: 1px solid #0AC8B9;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #006B93;
                }
            """
        else:  # skip button
            return """
                QPushButton {
                    background: transparent;
                    color: #785A28;
                    border: none;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    color: #C8AA6E;
                }
            """

class Tutorial:
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.steps: List[TutorialStep] = [
            TutorialStep(
                parent.block_toggle,
                "Welcome to Game Guardian! 🎮\n\n"
                "This is your main Guardian Shield. When activated, it prevents access "
                "to distracting applications, helping you stay focused."
            ),
            
            TutorialStep(
                parent.add_button,
                "Add Applications 📱\n\n"
                "Click here to choose which applications to protect yourself from. "
                "Select apps that tend to distract you during work or study time."
            ),
            
            TutorialStep(
                parent.app_list,
                "Protected Apps List 📋\n\n"
                "Your guarded applications appear here with their icons. "
                "These apps will be blocked when Guardian is active."
            ),
            
            TutorialStep(
                parent.remove_button,
                "Remove Apps ❌\n\n"
                "Select an app from the list and click here to remove it "
                "from your protected applications."
            ),
            
            TutorialStep(
                parent.downtime_toggle,
                "Full Lockdown Mode 🔒\n\n"
                "For maximum focus, enable this to block ALL applications "
                "except essential system processes. Perfect for deep work sessions."
            ),
            
            TutorialStep(
                None,
                "Password Protection 🔑\n\n"
                "Your settings are protected by a password. You'll need it to:"
                "\n• Enable/Disable Guardian"
                "\n• Modify blocked applications"
                "\n• Change protection settings",
                "center"
            ),
            
            TutorialStep(
                parent.findChild(QWidget, "HeaderSection"),
                "Time Restrictions ⏰\n\n"
                "Set up automatic blocking schedules for:"
                "\n• Study hours"
                "\n• Work focus time"
                "\n• Digital wellness breaks",
                "top"
            ),
            
            TutorialStep(
                None,
                "System Tray 💻\n\n"
                "Game Guardian runs in your system tray for easy access. "
                "Double-click the icon to show/hide the window.",
                "center"
            ),
            
            TutorialStep(
                parent,
                "Quick Tips 💡\n\n"
                "• Use Full Lockdown for important deadlines"
                "\n• Set up regular break schedules"
                "\n• Keep your password secure"
                "\n• Right-click tray icon for quick actions",
                "center"
            ),
            
            TutorialStep(
                parent.block_toggle,
                "Ready to Start! 🚀\n\n"
                "Click the Guardian Shield to begin protecting your focus time. "
                "You can replay this tutorial from the Help menu anytime.",
                "bottom"
            ),
            
            TutorialStep(
                None,
                "⚠️ Development Status ⚠️\n\n"
                "Currently, the app blocking features are in demonstration mode only.\n\n"
                "To make this a fully functional app like Cisdem, we need:\n"
                "• Apple Developer Account ($99/year)\n"
                "• Code signing and notarization\n"
                "• Proper App Store distribution\n\n"
                "This is a proof of concept showing the UI/UX and core functionality. "
                "With proper resources and V1 support, this could become a powerful "
                "focus-management tool for students and professionals.\n\n"
                "Thank you for checking out BuildBlock! 🙏",
                "center"
            )
        ]
        self.current_step = 0
    
    def start(self):
        """Start the tutorial"""
        if self.steps:
            self.show_step(0)
    
    def show_step(self, step_index: int):
        """Show a specific tutorial step"""
        if 0 <= step_index < len(self.steps):
            step = self.steps[step_index]
            popup = TutorialPopup(step.text, self.parent)
            
            # Position popup based on target and position
            if step.target:
                target_pos = step.target.mapToGlobal(QPoint(0, 0))
                if step.position == "bottom":
                    popup.move(target_pos.x(), target_pos.y() + step.target.height() + 10)
                elif step.position == "top":
                    popup.move(target_pos.x(), target_pos.y() - popup.height() - 10)
            else:
                # Center on screen for steps without specific targets
                center = self.parent.geometry().center()
                popup.move(center.x() - popup.width() // 2,
                          center.y() - popup.height() // 2)
            
            # Show popup with animation
            effect = QGraphicsOpacityEffect(popup)
            popup.setGraphicsEffect(effect)
            
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setDuration(300)
            anim.start()
            
            # Handle last step differently
            if step_index == len(self.steps) - 1:
                popup.setFinalStep(True)
            
            if popup.exec():
                self.current_step += 1
                if self.current_step < len(self.steps):
                    self.show_step(self.current_step) 