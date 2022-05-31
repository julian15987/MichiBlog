import json
from channels.generic.websocket import AsyncWebsocketConsumer
from MChat.models import MichiRoofs, MichiRoofUsers, MichiRoofChats
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    roof_group_name = None

    @database_sync_to_async
    def create_roof_add_michi(self, roof_id):
        try:
            new_roof = MichiRoofs.objects.get(roof_id=roof_id)
        except MichiRoofs.DoesNotExist:
            new_roof = MichiRoofs.objects.create(roof_id=roof_id, michi_owner=self.scope['user'].michiprofile)
        MichiRoofUsers.objects.get_or_create(roof_id=new_roof, user_id=self.scope['user'].michiprofile)

    @database_sync_to_async
    def add_michi_message(self, roof_id, message):
        roof = MichiRoofs.objects.get(roof_id=roof_id)
        MichiRoofChats.objects.create(roof_id=roof, michi_author=self.scope['user'].michiprofile, message=message)

    @database_sync_to_async
    def delete_roof(self, roof_id):
        MichiRoofs.objects.get(roof_id=roof_id).delete()

    @database_sync_to_async
    def delete_michi_from_roof(self, roof_id):
        try:
            MichiRoofUsers.objects.get(roof_id=roof_id, user_id=self.scope['user'].michiprofile).delete()
        except MichiRoofUsers.DoesNotExist:
            pass

    async def connect(self):
        roof_id = self.scope['url_route']['kwargs']['roof_id']
        self.roof_group_name = roof_id

        await self.channel_layer.group_add(
            self.roof_group_name,
            self.channel_name
        )

        await self.create_roof_add_michi(roof_id)
        await self.accept()

    async def disconnect(self, close_code):
        # await self.delete_michi_from_roof(self.roof_group_name)

        await self.channel_layer.group_discard(
            self.roof_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_img = text_data_json['user_img']
        timestamp = text_data_json['timestamp']
        user_nick = text_data_json['user_nick']

        await self.add_michi_message(self.roof_group_name, message)

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

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_img = event['user_img']
        timestamp = event['timestamp']
        user_nick = event['user_nick']

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'user_img': user_img,
            'message': message,
            'timestamp': timestamp,
            'user_nick': user_nick
        }))
