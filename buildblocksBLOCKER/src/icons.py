from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRect, QPoint, QSize

class GameIcons:
    @staticmethod
    def create_shield_icon(size=32):
        """Create shield icon for Guardian/Protection"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw shield shape
        painter.setPen(QPen(QColor("#785A28"), 2))
        painter.setBrush(QBrush(QColor("#005A82")))
        
        # Shield path
        path = QPainterPath()
        path.moveTo(size/2, 2)
        path.lineTo(size-4, size/3)
        path.lineTo(size-4, 2*size/3)
        path.quadTo(size/2, size-2, 4, 2*size/3)
        path.lineTo(4, size/3)
        path.lineTo(size/2, 2)
        
        painter.drawPath(path)
        painter.end()
        
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon

    @staticmethod
    def create_add_icon(size=32):
        """Create add application icon"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw plus symbol
        painter.setPen(QPen(QColor("#0AC8B9"), 2))
        painter.drawLine(size/4, size/2, 3*size/4, size/2)
        painter.drawLine(size/2, size/4, size/2, 3*size/4)
        
        painter.end()
        
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon

    @staticmethod
    def create_remove_icon(size=32):
        """Create remove application icon"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw minus symbol
        painter.setPen(QPen(QColor("#0AC8B9"), 2))
        painter.drawLine(size/4, size/2, 3*size/4, size/2)
        
        painter.end()
        
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon

    @staticmethod
    def create_time_icon(size=32):
        """Create time/schedule icon"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw clock circle
        painter.setPen(QPen(QColor("#785A28"), 2))
        painter.setBrush(QBrush(QColor("#005A82")))
        painter.drawEllipse(4, 4, size-8, size-8)
        
        # Draw clock hands
        painter.setPen(QPen(QColor("#0AC8B9"), 2))
        painter.drawLine(size/2, size/2, size/2, size/4)
        painter.drawLine(size/2, size/2, 3*size/4, size/2)
        
        painter.end()
        
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon

    @staticmethod
    def create_lockdown_icon(size=32):
        """Create lockdown/downtime icon"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw lock body
        painter.setPen(QPen(QColor("#785A28"), 2))
        painter.setBrush(QBrush(QColor("#005A82")))
        painter.drawRoundedRect(8, 14, 16, 14, 2, 2)
        
        # Draw lock shackle
        path = QPainterPath()
        path.moveTo(11, 14)
        path.lineTo(11, 10)
        path.arcTo(11, 6, 10, 8, 180, 180)
        path.lineTo(21, 14)
        
        painter.setPen(QPen(QColor("#785A28"), 2))
        painter.drawPath(path)
        
        painter.end()
        
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon 