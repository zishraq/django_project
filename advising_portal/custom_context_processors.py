from notification_system.models import BroadcastNotification


def notifications(request):
    all_notifications = BroadcastNotification.objects.all()[:5]
    view_notifications = []

    for notification in all_notifications:
        formatted_data = {
            'message': notification.message,
            'broadcast_at': notification.broadcast_at.strftime('%B %#d, %Y'),
            'sent': notification.sent
        }
        view_notifications.append(formatted_data)

    return {
        'notifications': view_notifications
    }
