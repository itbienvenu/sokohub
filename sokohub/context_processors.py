from django.conf import settings

def ai_settings(request):
    return {
        'encryption_key': getattr(settings, 'AI_ENCRYPTION_KEY', '')
    }
