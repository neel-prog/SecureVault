import os
import hashlib
import base64
from cryptography.fernet import Fernet

VAULT_DIR = os.path.join(os.getenv("APPDATA"), "SecureVault", "files")
os.makedirs(VAULT_DIR, exist_ok=True)

def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())


def encrypt_file(filepath, password):
    try:
        f = Fernet(generate_key(password))

        with open(filepath, "rb") as file:
            data = file.read()

        encrypted = f.encrypt(data)

        filename = os.path.basename(filepath) + ".enc"
        vault_path = os.path.join(VAULT_DIR, filename)

        with open(vault_path, "wb") as file:
            file.write(encrypted)

        return True, filename

    except Exception as e:
        return False, str(e)


def decrypt_file(filename, password, output_path):
    try:
        f = Fernet(generate_key(password))
        vault_path = os.path.join(VAULT_DIR, filename)

        with open(vault_path, "rb") as file:
            data = file.read()

        decrypted = f.decrypt(data)

        with open(output_path, "wb") as file:
            file.write(decrypted)

        return True, output_path

    except Exception as e:
        return False, str(e)

def list_files():
    try:
        return os.listdir(VAULT_DIR)
    except:
        return []

def delete_file(filename):
    try:
        path = os.path.join(VAULT_DIR, filename)
        os.remove(path)
        return True
    except Exception as e:
        return False