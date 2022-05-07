import json

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

            loop.run_until_complete(
                channel_layer.group_send(
                    # 'notification_broadcast',
                    f'notification_{notification.notification_to.username}',
                    {
                        'type': 'send_notification',
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
