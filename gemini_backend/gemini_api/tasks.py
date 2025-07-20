from celery import shared_task
from gemini_api.models import ChatRoom, Message
from .gemini import call_gemini

@shared_task
def handle_gemini_response(chatroom_id, prompt):
    response = call_gemini(prompt)
    Message.objects.create(chatroom_id=chatroom_id, sender="gemini", content=response)


    