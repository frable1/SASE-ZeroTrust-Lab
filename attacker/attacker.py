"""
Project: SASE-ZeroTrust-Lab
Module: attacker/attacker.py
Author: Francesco Ble
Date: 14th May 2026
Description: Malicious actor simulation. Tries to bypass SASE defenses.
"""

import requests
from core.crypto_engine import SASECryptomanager
import os
from dotenv import load_dotenv

def run_attack(scenario_name, headers=None, params=None):
    url = "http://127.0.0.1:8000/access"
    print(f"\n[Attack] Scenario: {scenario_name}")
    
    try:
        response = requests.post(url, headers=headers, params=params)
        print(f"[Gateway response] Status Code: {response.status_code}")
        print(f"[Gateway response] Detail: {response.json().get('detail')}")
    except Exception as e:
        print(f"[Error] Connection failed: {e}")

if __name__ == "__main__":
    print("Simulation launch attack on SASE systems")

    # Scenario 1: access without tokens - no identity
    run_attack("Anonymous access without token)")

    # Scenario 2: access with counterfeit token
    headers_fake = {"x-identity-token": "token_false_123_hack"}
    run_attack("Counterfeit token", headers=headers_fake)

    # Scenario 3: Unencrypted or corrupted payload
    headers_valid_structure = {"x-identity-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."} #Valid structure but not signed by us
    params_corrupt = {"encrypted_payload": "message_in_clear_not_encrypted"}
    run_attack("Clear payload - Bypass encryption", headers=headers_fake, params=params_corrupt)
    
    # Scenario 4: Valid identity but corrupt payload - to see the 400
    # We import the core to generate a valid token for testing
    load_dotenv()
    crypto_test = SASECryptomanager(os.getenv("MASTER_KEY").encode(), os.getenv("JWT_SECRET"))
    token_valido = crypto_test.generate_token("attaccante_astuto", "developer")
    
    headers_valid = {"x-identity-token": token_valido}
    params_malformed = {"encrypted_payload": "not_encrypted_garbage"}
    
    run_attack("Valid identity but corrupt payload", headers=headers_valid, params=params_malformed)