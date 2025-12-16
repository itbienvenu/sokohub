from django.test import TestCase, Client
from django.urls import reverse
from ai_assistant.security import EncryptionManager
from unittest.mock import patch
import json

class AIChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('ai_chat')
        self.encryption = EncryptionManager()
    
    @patch('ai_assistant.views.GroqService')
    def test_encrypted_chat_flow(self, mock_service_cls):
        # Mock the service response
        mock_instance = mock_service_cls.return_value
        mock_instance.process_message.return_value = "This is a mocked AI response."
        
        # Prepare encrypted payload
        payload_data = {
            "token": "some-uuid",
            "message": "Hello AI"
        }
        encrypted_payload = self.encryption.encrypt_data(payload_data)
        
        # Send Request
        response = self.client.post(
            self.url, 
            data=json.dumps({"payload": encrypted_payload}), 
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Decrypt Response
        response_json = response.json()
        self.assertIn("payload", response_json)
        
        decrypted_response = self.encryption.decrypt_data(response_json["payload"])
        self.assertEqual(decrypted_response["response"], "This is a mocked AI response.")
