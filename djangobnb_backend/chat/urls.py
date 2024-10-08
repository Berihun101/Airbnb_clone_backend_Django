from django.urls import path
from .api import conversations_list, conversation_detail, conversations_start

urlpatterns = [
    path('', conversations_list, name='conversations_list'),
    path('<uuid:id>/', conversation_detail, name='conversation_detail'),
    path('start/<uuid:user_id>/', conversations_start, name="start")
]