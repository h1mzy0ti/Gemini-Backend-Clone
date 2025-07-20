from celery import shared_task
from .models import ChatRoom, Message
from .gemini import call_gemini  

@shared_task
def handle_gemini_response(chatroom_id, user_message):
    room = None
    try:
        room = ChatRoom.objects.get(id=chatroom_id)

        # Call Gemini API
        gemini_reply = call_gemini(user_message)

        # Save Gemini's message
        Message.objects.create(chatroom=room, sender="gemini", content=gemini_reply)

    except Exception as e:
        if room:
            Message.objects.create(chatroom=room, sender="gemini", content="Error generating Gemini response.")
        print(f"[Gemini Task Error]: {e}")
