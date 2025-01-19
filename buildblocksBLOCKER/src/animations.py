from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt6.QtWidgets import QWidget

class GameAnimations:
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """Fade in animation for widgets"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation
    
    @staticmethod
    def button_press(widget: QWidget, duration: int = 100):
        """Button press animation"""
        animation = QPropertyAnimation(widget, b"size")
        original_size = widget.size()
        pressed_size = QSize(original_size.width() * 0.95, original_size.height() * 0.95)
        
        animation.setStartValue(original_size)
        animation.setEndValue(pressed_size)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        return animation
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = "right", duration: int = 300):
        """Slide in animation from specified direction"""
        animation = QPropertyAnimation(widget, b"pos")
        current_pos = widget.pos()
        
        if direction == "right":
            start_pos = QPoint(current_pos.x() + 100, current_pos.y())
        elif direction == "left":
            start_pos = QPoint(current_pos.x() - 100, current_pos.y())
        elif direction == "up":
            start_pos = QPoint(current_pos.x(), current_pos.y() - 100)
        else:  # down
            start_pos = QPoint(current_pos.x(), current_pos.y() + 100)
            
        animation.setStartValue(start_pos)
        animation.setEndValue(current_pos)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation 