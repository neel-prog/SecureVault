import hashlib
from sv_core.crypto import hash_password, verify_password

def hash_password_old(password):
    return hashlib.sha256(password.encode()).hexdigest()