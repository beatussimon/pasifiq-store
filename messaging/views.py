from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Message

@login_required
def inbox(request):
    messages_qs = Message.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'messaging/inbox.html', {'messages': messages_qs})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, user=request.user)
    if message.status == 'new':
        message.status = 'read'
        message.read_at = timezone.now()
        message.save()
    return render(request, 'messaging/detail.html', {'message': message})
