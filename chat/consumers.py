import json
from multiprocessing import context
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
import logging
from .models import Group, Message

User = get_user_model()

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        group=data['room']
        group = Group.objects.get(slug = group)
        messages = Message.load_message(group)
        print(messages)
        context = {
            'command' : 'messages',
            'messages' : self.messages_to_json(messages)
        }
        print(self.messages_to_json(messages))
        return self.send_message(context)

    def new_message(self, data):
        # self.chat_message
        author = data['from']
        group=data['room']
        group = Group.objects.get(slug = group)
        author_user = User.objects.filter(username = str(author))[0]
        message = Message.objects.create(
            author = author_user,
            content = data['message'],
            group = group
        )
        context = {
            'command': 'new_message',
            'message': self.msg_to_json(message),
        }
        return self.send_chat_message(context)

    def like_message(self,data):
        liked_by = data['liked_by']
        group=data['room']
        id=data['id']
        try:
            usr = User.objects.get(username=liked_by)
            msg = Message.objects.get(id=id)
            msg.like_message(usr)
        except:
            pass
        context = {
            'command': 'update_likes',
            'message': 'likes'
        }
        self.send_chat_message(context)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'like_message': like_message,
    }

    def messages_to_json(self, messages):
        return list(map(self.msg_to_json, messages))
    
    def msg_to_json(self, message, **kwargs):
        logger.warning('msg_to_json')
        return  {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.created),
            'likes' : str(message.likes_count()),
            'id': str(message.id)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name.replace('-','_')
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None):
        data = json.loads(text_data)
        logger.warning('recieved')
        self.commands[data['command']](self, data)
    
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))