"""
Project: SASE-ZeroTrust-Lab
Module: attacker/attacker.py
Author: Francesco Ble
Date: 14th May 2026
Description: Malicious actor simulation. Tries to bypass SASE defenses.
"""
import time
import requests
from core.crypto_engine import SASECryptomanager
import os
from dotenv import load_dotenv
import json

# Load environment variables - master key and JWT secret
load_dotenv()
URL = "http://127.0.0.1:8000/access"

def print_result(scenario, resp):
    """
    Helper function to format the output for each attack scenario.
    """
    print(f"Scenario: {scenario} ")
    print(f"Result: status code {resp.status_code}")
    print(f"Gateway response: {resp.json().get('detail', 'Success')}")
    print("-" * 45 + "\n")

def run_demo():
    print("SASE Security Gateway: interactive demo\n")
    
    # Initialize the crypto engine using keys from .env
    try:
        crypto = SASECryptomanager(
            os.getenv("MASTER_KEY").encode(), 
            os.getenv("JWT_SECRET")
        )
    except AttributeError:
        print("[Error] Keys not found. Please run setup_keys.py first.")
        return

    # 1. Anonymous access - missing token
    print("[TEST 1] Sending request without Identity Token...")
    r = requests.post(URL)
    print_result("Anonymous access", r)
    time.sleep(1.5)

    # 2. Identity spoofing - counterfeit token
    print("[TEST 2] Sending request with a Counterfeit Token...")
    # Manually creating a token with an invalid signature
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake_payload.fake_signature"
    r = requests.post(URL, headers={"x-identity-token": fake_token})
    print_result("Identity spoofing", r)
    time.sleep(1.5)

    # 3. Data tampering - valid identity but malformed ciphertext
    print("[TEST 3] Sending valid Identity but corrupted Ciphertext...")
    valid_token = crypto.generate_token("sase_identity_01", "developer")
    # Sending plain text instead of encrypted data to trigger decryption failure
    r = requests.post(
        URL, 
        headers={"x-identity-token": valid_token}, 
        params={"encrypted_payload": "garbage_unencrypted_data"}
    )
    print_result("Data tampering", r)
    time.sleep(1.5)

    # 4. Authorized access - the success baseline
    print("[TEST 4] Sending fully authorized SASE request...")
    # Let's turn the dictionary into a JSON string
    data_to_encrypt = json.dumps({"action": "read", "resource": "GitLab"})
    
    valid_payload = crypto.encrypt_data(data_to_encrypt)
    
    r = requests.post(URL, 
                      headers={"x-identity-token": valid_token}, 
                      params={"encrypted_payload": valid_payload})
    print_result("Authorized access", r)

if __name__ == "__main__":
    run_demo()