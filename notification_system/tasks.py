import json
import re

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification_system.models import BroadcastNotification

from celery import Celery, states
from celery.exceptions import Ignore
import asyncio


@shared_task(bind=True)
def broadcast_notification(self, data):
    print(data)

    try:
        notification = BroadcastNotification.objects.filter(id=int(data))

        if len(notification) > 0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()

            broadcast_at = notification.broadcast_at.strftime('%B %#d, %Y')

            user_id = str(notification.notification_to.id)

            loop.run_until_complete(
                channel_layer.group_send(
                    f'notification_{user_id}',
                    {
                        'type': 'send_notification',
                        'user': json.dumps(user_id),
                        'broadcast_at': json.dumps(broadcast_at),
                        'message': json.dumps(notification.message)
                    }
                )
            )
            notification.sent = True
            notification.save()
            return 'done'

        else:
            self.update_state(
                state='FAILURE',
                meta={
                    'exe': 'Not found'
                }
            )

            raise Ignore()

    except Exception:
        self.update_state(
            state='Failed',
            meta={
                'exe': 'Not found'
            }
        )

        raise Ignore()
