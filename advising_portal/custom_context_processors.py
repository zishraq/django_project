from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

from notification_system.models import BroadcastNotification


def notifications(request):
    view_notifications = []

    if request.user.is_authenticated:
        all_notifications = BroadcastNotification.objects.filter(notification_to=request.user)[:5]

        for notification in all_notifications:
            formatted_data = {
                'message': notification.message,
                'broadcast_at': notification.broadcast_at.strftime('%B %#d, %Y'),
                'sent': notification.sent,
                'notification_to': notification.notification_to,
                'notification_from': notification.notification_from,
                'link': notification.link
            }
            view_notifications.append(formatted_data)

    return {
        'notifications': view_notifications
    }
