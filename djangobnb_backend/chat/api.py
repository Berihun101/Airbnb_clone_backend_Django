from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes # type: ignore
from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from useraccount.models import User
@api_view(['GET'])
def conversations_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    return JsonResponse({
        'data': serializer.data
    }, safe=False)

@api_view(['GET'])
def conversation_detail(request, id):
    conversation = request.user.conversations.get(id=id)
    serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
    return JsonResponse({
        'conversation': serializer.data,
        'messages': messages_serializer.data
    }, safe=False)

@api_view(['GET'])
def conversations_start(request, user_id):
    conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

    if conversations.count() > 0:
        conversation = conversations.first()

        return JsonResponse({'success': True, 'conversation_id': conversation.id})
    else:
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)

        return JsonResponse({'success': True, 'conversation_id': conversation.id})