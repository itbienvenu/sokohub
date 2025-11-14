from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def register_user(validated_data):
    from accounts.serializers import RegisterSerializer
    serializer = RegisterSerializer(data=validated_data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    tokens = get_tokens_for_user(user)
    return user, tokens

def login_user(username, password):
    user = authenticate(username=username, password=password)
    if user:
        tokens = get_tokens_for_user(user)
        return user, tokens
    return None, None
