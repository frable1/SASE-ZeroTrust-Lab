"""
Project: SASE-ZeroTrust-Lab
Module: setup_keys.py
Author: Francesco Ble
Date: 14th May 2026
Description: Utility script to generate secure keys and environment variables.
"""
import secrets
from cryptography.fernet import Fernet


def generate_env_file():
    # Generate a valid AES-256 key for Fernet
    master_key = Fernet.generate_key().decode()
    # Generate a secure random secret for JWT tokens
    jwt_secret = secrets.token_hex(32)
    
    env_content = f"""# SASE Security Keys - Generated on 2026-05-14
    MASTER_KEY={master_key}
    JWT_SECRET={jwt_secret}
    """
    
    with open(".env", "w") as f:
        f.write(env_content)
        
    print("[SUCCESS] .env file created successfully.")
    print("Remember: This file should NOT be uploaded to GitHub!")
    
    #if __name__ == '__main__':
generate_env_file()
