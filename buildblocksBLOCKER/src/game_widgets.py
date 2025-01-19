from PyQt6.QtWidgets import QPushButton, QFrame, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient
from icons import GameIcons

class GameButton(QPushButton):
    def __init__(self, text, icon_type=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("GameButton")
        self.hover = False
        
        # Set icon based on button type
        if icon_type:
            self.setIcon(self._get_icon(icon_type))
            self.setIconSize(QSize(24, 24))
    
    def _get_icon(self, icon_type):
        icon_map = {
            "guardian": GameIcons.create_shield_icon,
            "add": GameIcons.create_add_icon,
            "remove": GameIcons.create_remove_icon,
            "time": GameIcons.create_time_icon,
            "lockdown": GameIcons.create_lockdown_icon
        }
        return icon_map.get(icon_type, lambda: None)()
    
    def enterEvent(self, event):
        self.hover = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.hover = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw button background with hover effect
        if self.hover:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#2F3B46"))
            gradient.setColorAt(1, QColor("#1E2328"))
            painter.fillRect(self.rect(), gradient)
        
        # Draw border
        border_color = QColor("#0AC8B9") if self.isChecked() else QColor("#785A28")
        painter.setPen(QPen(border_color, 2))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 3, 3)
        
        # Draw text and icon
        if self.icon():
            icon_rect = QRect(8, (self.height() - 24) // 2, 24, 24)
            self.icon().paint(painter, icon_rect)
            
        painter.setPen(QColor("#0AC8B9") if self.isChecked() else QColor("#C8AA6E"))
        text_rect = self.rect().adjusted(40, 0, -8, 0)  # Leave space for icon
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text()) 