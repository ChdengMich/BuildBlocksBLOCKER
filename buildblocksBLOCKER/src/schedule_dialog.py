from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTimeEdit, QListWidget, QLabel, QCheckBox)
from PyQt6.QtCore import QTime, Qt

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Time Restriction Manager")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Time selection
        time_layout = QHBoxLayout()
        self.start_time = QTimeEdit()
        self.end_time = QTimeEdit()
        time_layout.addWidget(QLabel("Start Time:"))
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(QLabel("End Time:"))
        time_layout.addWidget(self.end_time)
        layout.addLayout(time_layout)
        
        # Days selection
        days_layout = QHBoxLayout()
        self.day_checkboxes = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            checkbox = QCheckBox(day)
            self.day_checkboxes[day.lower()] = checkbox
            days_layout.addWidget(checkbox)
        layout.addLayout(days_layout)
        
        # Block all apps option
        self.block_all = QCheckBox("Block All Applications")
        self.block_all.toggled.connect(self._toggle_app_selection)
        layout.addWidget(self.block_all)
        
        # App selection
        self.app_list = QListWidget()
        self.app_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(QLabel("Select Apps to Block:"))
        layout.addWidget(self.app_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Schedule")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def _toggle_app_selection(self, checked):
        """Enable/disable app selection based on block all toggle"""
        self.app_list.setEnabled(not checked)
    
    def get_schedule(self) -> dict:
        """Get the schedule configuration"""
        selected_days = [day for day, cb in self.day_checkboxes.items() if cb.isChecked()]
        
        return {
            'days': selected_days,
            'start_time': self.start_time.time().toString('HH:mm'),
            'end_time': self.end_time.time().toString('HH:mm'),
            'apps': None if self.block_all.isChecked() else [
                self.app_list.item(i).data(Qt.ItemDataRole.UserRole)
                for i in range(self.app_list.count())
                if self.app_list.item(i).isSelected()
            ]
        } 