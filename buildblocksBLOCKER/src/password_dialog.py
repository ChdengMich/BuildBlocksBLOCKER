from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class PasswordDialog(QDialog):
    def __init__(self, parent=None, is_setup=False):
        super().__init__(parent)
        self.setWindowTitle("Password Required" if not is_setup else "Set Password")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        if is_setup:
            layout.addWidget(QLabel("Set a password to protect your settings:"))
        else:
            layout.addWidget(QLabel("Enter password to continue:"))
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        if is_setup:
            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setPlaceholderText("Confirm Password")
            layout.addWidget(self.confirm_input)
        
        self.submit_button = QPushButton("OK")
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)
        
        self.password_input.returnPressed.connect(self.submit_button.click)
    
    def get_password(self) -> str:
        return self.password_input.text()
    
    def get_confirmed_password(self) -> tuple[str, str]:
        return self.password_input.text(), self.confirm_input.text() 