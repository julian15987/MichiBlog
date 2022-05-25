import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    roof_name = None
    roof_group_name = None

    async def connect(self):
        self.roof_name = self.scope['url_route']['kwargs']['roof_name']
        self.roof_group_name = 'chat_%s' % self.roof_name

        # Join room group
        await self.channel_layer.group_add(
            self.roof_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.roof_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_img = text_data_json['user_img']
        timestamp = text_data_json['timestamp']
        user_nick = text_data_json['user_nick']


        print('--------')
        print(text_data_json)
        print(datetime.datetime.fromtimestamp(text_data_json['timestamp']/1000.0) - datetime.timedelta(hours=3))
        print('--------')

        # Send message to room group
        await self.channel_layer.group_send(
            self.roof_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'user_img': user_img,
                'message': message,
                'timestamp': timestamp,
                'user_nick': user_nick
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_img = event['user_img']
        timestamp = event['timestamp']
        user_nick = event['user_nick']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'user_img': user_img,
            'message': message,
            'timestamp': timestamp,
            'user_nick': user_nick
        }))
