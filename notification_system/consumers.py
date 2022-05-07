import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'notification_{self.room_name}'

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

    async def send_notification(self, event):
        message = json.loads(event['message'])
        broadcast_at = json.loads(event['broadcast_at'])

        # Send message to WebSocket

        await self.send(text_data=json.dumps({
            'broadcast_at': broadcast_at,
            'message': message
        }))

        # await self.send(text_data=json.dumps(message))
