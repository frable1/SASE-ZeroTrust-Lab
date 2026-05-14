"""
Project: SASE-ZeroTrust-Lab
Module: client/client.py
Author: Francesco Ble
Date: 14th May 2026
Description: Authorized client. Generates identity tokens and sends encrypted traffic.
"""

import requests
import os
from dotenv import load_dotenv
from core.crypto_engine import SASECryptomanager

# Load security keys from the.env file
load_dotenv()

# Let's initialize the cryptographic engine
crypto = SASECryptomanager(
    master_key=os.getenv("MASTER_KEY").encode(),
    jwt_secret=os.getenv("JWT_SECRET")
)

def send_secure_request(user_id: str, role: str, message: str):
    url = "http://127.0.0.1:8000/access"
    
    print(f"\n[Client] Preparation required for: {user_id} ({role})")
    
    # 1. Identity token generation - Zero Trust
    token = crypto.generate_token(user_id, role)
    print(f"[Client] Generated JWT token: {token[:20]}...")
    # 2. Data encryption - Privacy
    encrypted_msg = crypto.encrypt_data(message).decode()
    print(f"[Client] Cipher: {encrypted_msg[:20]}...")
    # 3. Sending the request to the SASE Gateway
    headers = {"x-identity-token": token}
    params = {"encrypted_payload": encrypted_msg}
    
    try:
        response = requests.post(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print("\n[Success] Response from Gateway:")
            print(response.json())
        else:
            print(f"\n[Failed] Status: {response.status_code}")
            print(f"Detail: {response.json().get('detail')}")
    except Exception as e:
        print(f"[Error] Connection failed: {e}")

if __name__ == "__main__":
    # Simulate access by an authorized user
    send_secure_request(
        user_id="francesco_dev",
        role="developer",
        message="Request access to the internal GitLab server."
    )
