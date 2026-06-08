import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a key from the given password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))
salt = os.urandom(16)
key = derive_key("my_secure_password", salt)
print(key)

# Example usage of the derived key with Fernet for encryption
fernet = Fernet(key)
message = "This is a secret message."
encrypted_message = fernet.encrypt(message.encode())
print(f"Encrypted message: {encrypted_message}")
decrypted_message = fernet.decrypt(encrypted_message).decode()
print(f"Decrypted message: {decrypted_message}")