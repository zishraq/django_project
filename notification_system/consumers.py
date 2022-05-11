import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'notification_{self.room_name}'

        # print(self.room_name)
        # print(self.scope)
        # print(self.scope['user'])

        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_notification(self, event):
        message = json.loads(event['message'])
        broadcast_at = json.loads(event['broadcast_at'])

        # Send message to WebSocket

        # print('---------------------------', dir(self))
        # print('-----', event)
        # print('-----', self.scope)
        # print('-----', self.scope['user'])
        # print('-----', self.room_name)
        # print('-----', self.room_group_name)

        await self.send(text_data=json.dumps({
            'broadcast_at': broadcast_at,
            'message': message
        }))

        # await self.send(text_data=json.dumps(message))
