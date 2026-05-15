"""
Project: SASE-ZeroTrust-Lab
Module: gateway/main.py
Author: Francesco Ble
Date: 14th May 2026
Description: SASE Gateway PoP. Implements identity validation and traffic decryption.
"""

from fastapi import FastAPI, Header, HTTPException
from core.crypto_engine import SASECryptomanager
import os
from dotenv import load_dotenv

# Load keys from the generated .env file
load_dotenv()

app = FastAPI(title="SASE PoP Gateway")

# Let's initialize the cryptographic handler
crypto = SASECryptomanager(
    master_key=os.getenv("MASTER_KEY").encode(),
    jwt_secret=os.getenv("JWT_SECRET")
)

@app.get("/")
def health_check():
    return {"status": "SASE Gateway Online", "protection": "Zero Trust Active"}

@app.post("/access")
async def secure_access(x_identity_token: str = Header(None), encrypted_payload: str = None):
    """
    Endpoint simulating traffic inspection.
    """
    if not x_identity_token:
        raise HTTPException(status_code=401, detail="Identity Token Missing")
    
    # 1. Identity Validation (Who are you?)
    user_data = crypto.verify_token(x_identity_token)
    if not user_data:
        raise HTTPException(status_code=403, detail="Invalid Token")
    
    # 2. Deciphering (What are you sending?)
    try: 
        decrypted_message = crypto.decrypt_data(encrypted_payload.encode())
        return {
            "status": "ACCESS GRANTED",
            "identity": user_data,
            "message": decrypted_message
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption Failed")