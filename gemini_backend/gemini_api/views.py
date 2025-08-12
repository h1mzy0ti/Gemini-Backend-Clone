from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
from .models import ChatRoom, Message
from .serializers import *
from subscriptions.models import Subscription  # From subscriptions app
from .tasks import handle_gemini_response


'''
Handles /chatroom/ endpoint for creating a chatroom and Listing chatrooms
'''
class ChatRoomCreatList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"user_chatrooms_{request.user.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        rooms = ChatRoom.objects.filter(user=request.user)
        data = ChatRoomSerializer(rooms, many=True).data
        cache.set(cache_key, data, timeout=300)
        return Response(data,status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get("title", "Untitled")
        chatroom = ChatRoom.objects.create(user=request.user, title=title)
        cache.delete(f"user_chatrooms_{request.user.id}")
        return Response(ChatRoomSerializer(chatroom).data, status=status.HTTP_201_CREATED)


'''
Handles /chatroom/<int:id>/ endpoint for listing chatroom by id
and deleting a chatroom by id
'''
class ChatRoomDeleteDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            room = ChatRoom.objects.get(id=id, user=request.user)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chatroom doesnt exist or Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ChatRoomSerializer(room).data,status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            room = ChatRoom.objects.get(id=id, user=request.user)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        room.delete()
        cache.delete(f"user_chatrooms_{request.user.id}")
        return Response({"status": "ChatRoom deleted successfully"}, status=status.HTTP_202_ACCEPTED)

'''
Handles /chatroom/<int:id>/message/ endpoint for sending messages 
and recieving messages
'''
class ChatMessageSendRecieve(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        content = request.data.get("content", "").strip()
        if not content:
            return Response({"error": "Empty message"}, status=400)

        try:
            room = ChatRoom.objects.get(id=id, user=request.user)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room does not exist or not found"}, status=status.HTTP_404_NOT_FOUND)

        # Rate limiting for Basic plan users
        sub = Subscription.objects.filter(user=request.user).first()
        today = timezone.now().date()

        if sub and sub.plan == 'basic':
            if sub.last_reset != today:
                sub.daily_message_count = 0
                sub.last_reset = today
                sub.save()

            if sub.daily_message_count >= 5:
                return Response({"error": "Daily message limit reached"}, status=status.HTTP_402_PAYMENT_REQUIRED)

            sub.daily_message_count += 1
            sub.save()

        # Save user's message
        Message.objects.create(chatroom=room, sender="user", content=content)

        # Call Gemini asynchronously via Celery
        handle_gemini_response.delay(room.id, content)

        return Response({"status": "Message sent, Gemini response queued, refer a get request in the same endpoint"}, status=status.HTTP_201_CREATED)

    def get(self, request, id):
        try:
            room = ChatRoom.objects.get(id=id, user=request.user)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room doesnt exist or Not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(chatroom=room).order_by("timestamp")
        data = MessageSerializer(messages, many=True).data
        return Response(data,status=status.HTTP_200_OK)

class ReversedValid(APIView):
    def post(self,request):
        data = request.data
        if data.is_valid():
            ReversedValidSerilizr = ReversedValidSerilizr(data)
            return Response({"Message":"success"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):

        returndata = request.query_param.get('text', '')

        serilizer = ReversedValidSerilizr({'original': text})
        return Response(serilizer.data)