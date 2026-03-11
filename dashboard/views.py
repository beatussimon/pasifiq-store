from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from .decorators import owner_required
from .forms import ProductForm, ProductImageForm, CategoryForm, SiteSettingsForm
from products.models import Product, ProductImage
from categories.models import Category
from messaging.models import Message
from users.models import CustomUser
from analytics.models import ProductView, DailyStats
from notifications.models import Notification
from core.models import SiteSettings

from analytics.utils import get_daily_stats

@owner_required
def dashboard_index(request):
    # Stats
    total_products = Product.objects.filter(is_active=True).count()
    total_users = CustomUser.objects.filter(is_active=True).count()
    total_messages = Message.objects.count()
    new_messages = Message.objects.filter(status='new').count()
    
    # Most viewed products
    top_viewed = Product.objects.filter(is_active=True).order_by('-view_count')[:5]
    top_wished = Product.objects.filter(is_active=True).order_by('-wishlist_count')[:5]
    top_inquired = Product.objects.filter(is_active=True).order_by('-inquiry_count')[:5]
    
    # Recent messages
    recent_messages = Message.objects.select_related('product').order_by('-created_at')[:5]
    
    # Charts data
    stats = get_daily_stats(7)
    
    # Recent notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]
    
    return render(request, 'dashboard/index.html', {
        'total_products': total_products,
        'total_users': total_users,
        'total_messages': total_messages,
        'new_messages': new_messages,
        'top_viewed': top_viewed,
        'top_wished': top_wished,
        'top_inquired': top_inquired,
        'recent_messages': recent_messages,
        'chart_days': stats['days'],
        'chart_views': stats['views'],
        'chart_inquiries': stats['inquiries'],
        'notifications': notifications,
    })

from products.utils import get_filtered_products

@owner_required
def product_list(request):
    products = get_filtered_products(request, queryset=Product.objects.all())
    
    paginator = Paginator(products, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'dashboard/product_list.html', {
        'products': page,
        'categories': categories,
        'search': request.GET.get('q', ''),
        'selected_status': request.GET.get('status', ''),
        'selected_category': request.GET.get('category', ''),
    })

@owner_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            # Handle image upload
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=img,
                    is_primary=(i == 0),
                    sort_order=i
                )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Create Product'})

@owner_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            # Handle new images
            new_images = request.FILES.getlist('images')
            existing_count = product.images.count()
            for i, img in enumerate(new_images):
                ProductImage.objects.create(
                    product=product,
                    image=img,
                    is_primary=(existing_count == 0 and i == 0),
                    sort_order=existing_count + i
                )
            messages.success(request, f'Product "{product.name}" updated.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {
        'form': form, 'product': product, 'title': 'Edit Product'
    })

@owner_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/confirm_delete.html', {'product': product})

@owner_required
def toggle_featured(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_featured = not product.is_featured
    product.save(update_fields=['is_featured'])
    status = 'featured' if product.is_featured else 'unfeatured'
    messages.success(request, f'Product {status}.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:product_list'))

@owner_required
def product_images(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        existing = product.images.count()
        for i, img in enumerate(images):
            ProductImage.objects.create(product=product, image=img, sort_order=existing+i)
        messages.success(request, f'{len(images)} image(s) uploaded.')
    return render(request, 'dashboard/product_images.html', {'product': product})

@owner_required
def delete_image(request, image_id):
    image = get_object_or_404(ProductImage, pk=image_id)
    product_id = image.product_id
    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('dashboard:product_images', product_id=product_id)

@owner_required
def message_list(request):
    msgs = Message.objects.select_related('product', 'user').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        msgs = msgs.filter(status=status_filter)
    paginator = Paginator(msgs, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'dashboard/message_list.html', {
        'messages': page,
        'status_filter': status_filter or '',
        'new_count': Message.objects.filter(status='new').count(),
    })

@owner_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.status == 'new':
        message.status = 'read'
        message.read_at = timezone.now()
        message.save()
        Notification.objects.filter(
            recipient=request.user,
            notification_type='inquiry',
            is_read=False
        ).filter(link__contains=f'/dashboard/messages/{pk}/').update(is_read=True)
    return render(request, 'dashboard/message_detail.html', {'message': message})

@owner_required
def archive_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.status = 'archived'
    message.save()
    messages.success(request, 'Message archived.')
    return redirect('dashboard:message_list')

@owner_required
def user_list(request):
    users = CustomUser.objects.filter(is_superuser=False).order_by('-date_joined')
    paginator = Paginator(users, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'dashboard/user_list.html', {'users': page})

@owner_required
def analytics_view(request):
    days_range = 30
    stats = get_daily_stats(days_range)
    
    top_products = Product.objects.filter(is_active=True).order_by('-view_count')[:10]
    
    return render(request, 'dashboard/analytics.html', {
        'chart_days': stats['days'],
        'chart_views': stats['views'],
        'chart_inquiries': stats['inquiries'],
        'chart_registrations': stats['registrations'],
        'top_products': top_products,
        'total_views': sum(stats['views']),
        'total_inquiries': sum(stats['inquiries']),
        'total_registrations': sum(stats['registrations']),
    })

@owner_required
def category_list(request):
    cats = Category.objects.prefetch_related('children', 'products').order_by('sort_order', 'name')
    return render(request, 'dashboard/category_list.html', {'categories': cats})

@owner_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f'Category "{cat.name}" created.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Create Category'})

@owner_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'category': category, 'title': 'Edit Category'})

@owner_required
def store_settings(request):
    settings_obj = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store settings updated.')
            return redirect('dashboard:settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    return render(request, 'dashboard/settings.html', {'form': form})
