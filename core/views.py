from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from products.models import Product
from categories.models import Category
from messaging.models import Message
from messaging.forms import MessageForm

def home(request):
    featured = Product.objects.filter(is_featured=True, is_active=True).select_related('category').prefetch_related('images')[:8]
    latest = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')[:8]
    popular = Product.objects.filter(is_active=True).order_by('-view_count').select_related('category').prefetch_related('images')[:8]
    categories = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')[:8]
    return render(request, 'core/home.html', {
        'featured_products': featured,
        'latest_products': latest,
        'popular_products': popular,
        'categories': categories,
    })

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.ip_address = request.META.get('REMOTE_ADDR')
            msg.save()
            # Notify store owner
            try:
                from notifications.utils import notify_owner_new_inquiry
                notify_owner_new_inquiry(msg)
            except:
                pass
            from django.contrib import messages
            messages.success(request, 'Your message has been sent! We will contact you shortly.')
            return redirect('core:contact')
    else:
        if request.user.is_authenticated:
            form = MessageForm(initial={
                'sender_name': request.user.get_full_name() or request.user.username,
                'sender_email': request.user.email,
                'sender_phone': request.user.phone,
            })
        else:
            form = MessageForm()
    return render(request, 'core/contact.html', {'form': form})

def robots_txt(request):
    content = "User-agent: *\nDisallow: /admin/\nDisallow: /dashboard/\nSitemap: /sitemap.xml"
    return HttpResponse(content, content_type='text/plain')
