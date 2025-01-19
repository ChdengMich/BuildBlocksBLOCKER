import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Security:
    def __init__(self):
        self._key = None
        self._fernet = None
    
    def set_password(self, password: str) -> bytes:
        """Set up encryption with the given password"""
        if not password:
            raise ValueError("Password cannot be empty")
            
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self._key = key
        self._fernet = Fernet(key)
        return salt
        
    def verify_password(self, password: str, salt: bytes) -> bool:
        """Verify if the provided password matches the stored one"""
        if not password or not salt:
            return False
            
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key == self._key
        except Exception:
            return False
    
    def load_key(self, password: str, salt: bytes) -> bool:
        """Load encryption key from password"""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self._key = key
            self._fernet = Fernet(key)
            return True
        except Exception:
            return False 