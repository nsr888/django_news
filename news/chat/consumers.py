import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, ChatRoom
from django.contrib.auth.models import User
import time

class ChatConsumer(WebsocketConsumer):
    lastPing = 100*[0.00]

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json['message_type']
        user_id = text_data_json['user_id']

        chatroom = ChatRoom.objects.get(id = self.room_id) 
        user = User.objects.get(id = user_id)
        user_name = user.username
        if not message_type:
            message_o = Message(chatroom=chatroom, user=user, message=message)
            message_o.save()
        if message_type == 3:
            # print("ping", user_name)
            # print("diff", time.time() - self.lastPing[user_id])
            self.lastPing[user_id] = time.time()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type' : message_type,
                'user_id': user_id,
                'user_name': user_name
            }
        )
        for idx, val in enumerate(self.lastPing):
            if val and time.time() - val > 3:
                self.lastPing[idx] = 0
                print("exit: ", idx)
                # Send message to room group
                user_name = User.objects.get(id = idx).username
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': user_name + ' has left the chat',
                        'message_type' : 2,
                        'user_id': idx,
                        'user_name': user_name
                    }
                )

    # Receive message from room group
    def chat_message(self, event):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        message = event['message']
        user_name = event['user_name']
        message_type = event['message_type']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_type' : message_type,
            'user_name': user_name
        }))
