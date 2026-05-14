"""
Project: SASE-ZeroTrust-Lab
Module: core/crypto_engine.py
Author: Francesco Ble
Date: 14th May 2026
Description: Managing symmetric encryption and JWT identity tokens.
"""
import jwt
import datetime
from cryptography.fernet import Fernet
from typing import Optional, Dict

class SASECryptomanager:
    def __init__(self, master_key: butes, jwt_secret: str):
        """
        Initialize the cryptographic manager.
        :param master_key: Data encryption key (AES-256 sim).
        :param jwt_secret: Secret for signing identity tokens.
        """
        self.cipher = Fernet(master_key)
        self.jwt_secret = jwt_secret
    
    # Identity section - Zero Trust
    def generate_token(self, user_id: str, role: str) -> str:
        """
        Create a JWT token for the user. 
        Demonstrates the concept of 'Identity-as-a-Perimeter'.
        """
        payload={
            "sub": user_id,
            "role": role,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime-timedelta(minutes=30)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Check if the token is valid and not counterfeit."""
        try: 
            return jwt.decode(token, self.jwt_secret, algorithm=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        

    # Privacy section - Data-In-Transit
    def encrypt_data(self, message: str) -> bytes:
        """It encrypts the message to simulate its transit through a safe tunnel."""
        return self.cipher.encrypt(message.encode())
    
    def decrypt_data(self, encrypted_bytes: bytes) -> str:
        """Decrypts the message received from the gateway."""
        return self.cipher.decrypt(encrypted_bytes).decode()