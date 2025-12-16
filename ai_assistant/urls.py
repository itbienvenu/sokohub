from django.urls import path
from .views import AIChatView, chat_page

urlpatterns = [
    path('', chat_page, name='ai_chat_page'),
    path('chat/', AIChatView.as_view(), name='ai_chat'),
]
