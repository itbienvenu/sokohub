import base64
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings

class EncryptionManager:
    def __init__(self):
        # We need a 32-byte key for AES-256
        raw_key = getattr(settings, 'AI_ENCRYPTION_KEY', '')
        if not raw_key:
            raw_key = 'default-insecure-key-for-dev'
        
        # Ensure key is 32 bytes (SHA-256 is a good way to get 32 bytes from any string)
        self.key = hashlib.sha256(raw_key.encode()).digest()
        
    def encrypt_data(self, data):
        """Encrypts a dictionary or list into a base64 string using AES-CBC."""
        try:
            json_data = json.dumps(data)
            # IV must be 16 bytes. Random for security.
            iv = b'0000000000000000' # FIXED IV for simplicity matching with JS without complex exchange, 
                                     # OR better: generate random, prepend to ciphertext.
                                     # For this requirement, let's use a random IV and encode it.
            
            cipher = AES.new(self.key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(json_data.encode(), AES.block_size))
            
            # Return IV + Ciphertext encoded in Base64
            # Format: iv:ciphertext
            iv_b64 = base64.b64encode(cipher.iv).decode('utf-8')
            ct_b64 = base64.b64encode(ct_bytes).decode('utf-8')
            return f"{iv_b64}:{ct_b64}"
            
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt_data(self, payload):
        """Decrypts a base64 string payload."""
        try:
            iv_b64, ct_b64 = payload.split(':')
            iv = base64.b64decode(iv_b64)
            ct = base64.b64decode(ct_b64)
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return json.loads(pt.decode('utf-8'))
        except Exception as e:
            # print(f"Decryption error: {e}")
            raise ValueError("Invalid token or decryption failed") from e
