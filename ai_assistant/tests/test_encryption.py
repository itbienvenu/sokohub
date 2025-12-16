from django.test import TestCase
from ai_assistant.security import EncryptionManager
import json

class EncryptionTest(TestCase):
    def setUp(self):
        self.manager = EncryptionManager()

    def test_encrypt_decrypt(self):
        data = {"message": "hello world", "token": "123"}
        encrypted = self.manager.encrypt_data(data)
        self.assertNotEqual(encrypted, json.dumps(data))
        
        decrypted = self.manager.decrypt_data(encrypted)
        self.assertEqual(decrypted, data)

    def test_invalid_decrypt(self):
        with self.assertRaises(ValueError):
            self.manager.decrypt_data("invalid_token_string")
