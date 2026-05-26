import hashlib
import hmac
import os
import base64
from cryptography.fernet import Fernet

# ── Encryption (unchanged) ─────────────────────────────────────────────────

def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt(text, password):
    return Fernet(generate_key(password)).encrypt(text.encode())

def decrypt(token, password):
    return Fernet(generate_key(password)).decrypt(token).decode()

# ── PBKDF2 Password Hashing (new) ──────────────────────────────────────────

PBKDF2_HASH_ALGO  = "sha256"
PBKDF2_ITERATIONS = 600_000
PBKDF2_SALT_BYTES = 32
PBKDF2_HASH_BYTES = 32
SEPARATOR         = "$"

def hash_password(password: str) -> str:
    salt = os.urandom(PBKDF2_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(
        PBKDF2_HASH_ALGO,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=PBKDF2_HASH_BYTES,
    )
    return SEPARATOR.join([
        PBKDF2_HASH_ALGO,
        str(PBKDF2_ITERATIONS),
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(dk).decode("ascii"),
    ])

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algo, iters, b64salt, b64hash = stored_hash.split(SEPARATOR)
        salt     = base64.b64decode(b64salt)
        expected = base64.b64decode(b64hash)
    except ValueError:
        return False
    dk = hashlib.pbkdf2_hmac(
        algo,
        password.encode("utf-8"),
        salt,
        int(iters),
        dklen=len(expected),
    )
    return hmac.compare_digest(dk, expected)