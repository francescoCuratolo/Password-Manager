import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(password: str, salt: bytes, lenght=32) -> bytes:
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=lenght,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )

    return kdf.derive(password.encode())

def generate_master_password(master_password: str):

    salt = os.urandom(16)
    master_hash = derive_key(master_password, salt)

    data = {
        "master": {
            "salt": base64.b64encode(salt).decode(),
            "hash": base64.b64encode(master_hash).decode()
        }
    }

    return data


def encrypt_password(aes_key: bytes, plaintext: str) -> dict:

    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

    return {
        "nonce": base64.b64encode(nonce).decode(),
        "password": base64.b64encode(ciphertext).decode()
    }

def decrypt_password(aes_key: bytes, enc_data: dict) -> str:
    
    aesgcm = AESGCM(aes_key)

    nonce = base64.b64decode(enc_data["nonce"])
    ciphertext = base64.b64decode(enc_data["password"])

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()


