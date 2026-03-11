from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated and (request.user.is_store_owner or request.user.is_superuser):
        unread = Notification.objects.filter(recipient=request.user, is_read=False).count()
        recent = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
    else:
        unread = 0
        recent = []
    return {'unread_notifications': unread, 'recent_notifications': recent}
