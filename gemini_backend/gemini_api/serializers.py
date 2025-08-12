# serializers.py
from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ReversedValidSerilizr(serializers.Serializer):
    origin = serializers.CharField(write_only=True,blank=False)
    reversedstring = serializers.SerializerMethodField()
    
    def reverse(self,object):
        
        originalString = getattr(object, 'Original',None) or object.get('original')
        if originalString:
            return originalString[::-1]
        return originalString.error