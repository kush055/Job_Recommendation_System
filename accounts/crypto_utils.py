import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from django.conf import settings


def load_private_key():
    """
    Load RSA private key from a PEM file.
    """
    private_key_path = settings.PRIVATE_KEY_PATH

    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Set password here if your private key is encrypted
        )

    return private_key


def decrypt_with_private_key(enc_key_b64: str) -> str:
    """
    Decrypts a base64-encoded string (RSA-encrypted AES key from frontend).
    
    :param enc_key_b64: Base64-encoded encrypted AES key
    :return: Decrypted AES key string
    """
    try:
        encrypted_data = base64.b64decode(enc_key_b64)
    except Exception as e:
        raise ValueError(f"Base64 decoding failed: {str(e)}")

    private_key = load_private_key()

    try:
        decrypted_data = private_key.decrypt(
            encrypted_data,
            asym_padding.PKCS1v15()  # Must match frontend's JSEncrypt padding
        )
        return decrypted_data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"RSA decryption failed: {str(e)}")
