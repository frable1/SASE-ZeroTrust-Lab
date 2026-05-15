import pytest
import requests
import os
import json
from core.crypto_engine import SASECryptomanager
from dotenv import load_dotenv

# Load keys from the .env file
load_dotenv()

URL = "http://127.0.0.1:8000/access"

@pytest.fixture
def crypto():
    """Initializes the cryptographic engine for testing."""
    master_key = os.getenv("MASTER_KEY")
    jwt_secret = os.getenv("JWT_SECRET")
    
    if not master_key or not jwt_secret:
        pytest.fail("Keys not found in the.env file. Run setup_keys.py first!")
        
    return SASECryptomanager(master_key.encode(), jwt_secret)

def test_security_logic_flow(crypto):
    """
    Test the entire security pipeline of the Gateway SASE.
    Verification: 401 (No token), 403 (Invalid token), 400 (Invalid payment), 200 (Success).
    """
    
    # TEST 1: Anonymous Access - No Token
    # We expect 401 Unauthorized
    response_1 = requests.post(URL)
    assert response_1.status_code == 401
    
    # TEST 2: False identity - Invalid Token
    # We expect 403 Forbidden
    headers_fake = {"x-identity-token": "token.false.incorrect_signature"}
    response_2 = requests.post(URL, headers=headers_fake)
    assert response_2.status_code == 403
    
    # TEST 3: Valid identity but corrupted data
    # We expect 400 bad requests
    token = crypto.generate_token("test_user", "tester")
    params_corrupt = {"encrypted_payload": "garbage_un_encrypted_data"}
    response_3 = requests.post(URL, headers={"x-identity-token": token}, params=params_corrupt)
    assert response_3.status_code == 400
    
    # TEST 4: Legitimate Flow - Authorized Access
    # We expect 200 OK
    data_to_send = json.dumps({"action": "test", "status": "working"})
    valid_payload = crypto.encrypt_data(data_to_send)
    response_4 = requests.post(
        URL, 
        headers={"x-identity-token": token}, 
        params={"encrypted_payload": valid_payload}
    )
    
    assert response_4.status_code == 200
    assert response_4.json().get("status") == "ACCESS GRANTED"