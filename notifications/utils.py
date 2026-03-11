from django.conf import settings

def get_store_owner():
    from users.models import CustomUser
    return CustomUser.objects.filter(is_store_owner=True).first() or CustomUser.objects.filter(is_superuser=True).first()

def notify_owner_new_inquiry(message):
    owner = get_store_owner()
    if not owner:
        return
    from .models import Notification
    from django.urls import reverse
    Notification.objects.create(
        recipient=owner,
        notification_type='inquiry',
        title=f'New inquiry from {message.sender_name}',
        message=f'Product: {message.product.name if message.product else "General"}\n{message.content[:100]}',
        link=f'/dashboard/messages/{message.pk}/',
    )

def notify_owner_new_rating(rating):
    owner = get_store_owner()
    if not owner:
        return
    from .models import Notification
    Notification.objects.create(
        recipient=owner,
        notification_type='rating',
        title=f'New {rating.score}★ rating on {rating.product.name}',
        message=f'From {rating.user.username}: {rating.review[:100]}' if rating.review else f'From {rating.user.username}',
        link=rating.product.get_absolute_url(),
    )
