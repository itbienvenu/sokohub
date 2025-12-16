from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import json
from .security import EncryptionManager
from .services import GroqService

@login_required
def chat_page(request):
    return render(request, 'ai_assistant/chat.html', {
        'encryption_key': getattr(settings, 'AI_ENCRYPTION_KEY', '')
    })

@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(View):
    def post(self, request, *args, **kwargs):
        # 1. Decrypt Request
        encryption = EncryptionManager()
        try:
             # We expect a JSON body with {"payload": "encrypted_string"}
            body = json.loads(request.body)
            encrypted_payload = body.get('payload')
            
            if not encrypted_payload:
                return JsonResponse({"error": "Missing payload"}, status=400)
            
            data = encryption.decrypt_data(encrypted_payload)
            
        except Exception as e:
            return JsonResponse({"error": "Decryption failed or invalid format"}, status=400)

        # 2. Extract Data
        token = data.get('token')
        message = data.get('message')
        
        request_user_id = request.user.id if request.user.is_authenticated else None
        payload_user_id = data.get('user_id')
        
        if payload_user_id and request_user_id and payload_user_id != request_user_id:
             pass

        if not message:
            return JsonResponse({"error": "Message is required"}, status=400)

        # 3. Process with AI
        service = GroqService()
        try:
            response_text = service.process_message(token, message, request.user)
        except Exception as e:
            # Log error
            return JsonResponse({"error": str(e)}, status=500)

        # 4. Encrypt Response
        response_data = {
            "response": response_text
        }
        encrypted_response = encryption.encrypt_data(response_data)

        return JsonResponse({"payload": encrypted_response})
