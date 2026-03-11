from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, ProductImage
from categories.models import Category
from messaging.forms import MessageForm

from .utils import get_filtered_products

def product_list(request):
    products = get_filtered_products(request)
    categories = Category.objects.filter(is_active=True)
    
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'products/list.html', {
        'products': page,
        'categories': categories,
        'selected_category': request.GET.get('category'),
        'selected_condition': request.GET.get('condition'),
        'selected_status': request.GET.get('status'),
        'sort': request.GET.get('sort', '-created_at'),
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Track view
    _track_view(request, product)
    
    # Related products
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk).prefetch_related('images')[:4]
    
    # Check user status
    in_wishlist = False
    in_saved = False
    user_rating = None
    if request.user.is_authenticated:
        from wishlist.models import WishlistItem
        from saved_items.models import SavedItem
        from ratings.models import Rating
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
        in_saved = SavedItem.objects.filter(user=request.user, product=product).exists()
        try:
            user_rating = Rating.objects.get(user=request.user, product=product)
        except Rating.DoesNotExist:
            pass
    
    # Ratings distribution
    from ratings.models import Rating
    all_ratings = Rating.objects.filter(product=product).order_by('-created_at')
    total_ratings = all_ratings.count()
    rating_dist_with_pct = {}
    for i in range(5, 0, -1):
        count = all_ratings.filter(score=i).count()
        pct = (count / total_ratings * 100) if total_ratings > 0 else 0
        rating_dist_with_pct[i] = {'count': count, 'pct': pct}
    
    # Contact form
    contact_form = MessageForm(initial={'sender_name': request.user.get_full_name() if request.user.is_authenticated else ''})
    
    return render(request, 'products/detail.html', {
        'product': product,
        'related_products': related,
        'in_wishlist': in_wishlist,
        'in_saved': in_saved,
        'user_rating': user_rating,
        'all_ratings': all_ratings[:10],
        'rating_dist_with_pct': rating_dist_with_pct,
        'contact_form': contact_form,
    })

def product_contact(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.product = product
            if request.user.is_authenticated:
                msg.user = request.user
            msg.ip_address = request.META.get('REMOTE_ADDR')
            msg.save()
            product.inquiry_count += 1
            product.save(update_fields=['inquiry_count'])
            try:
                from notifications.utils import notify_owner_new_inquiry
                notify_owner_new_inquiry(msg)
            except:
                pass
            messages.success(request, 'Inquiry sent! We will contact you soon.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return redirect('products:detail', slug=slug)

def _track_view(request, product):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    from analytics.models import ProductView
    from django.utils import timezone
    
    from django.db.models import F
    # Only count once per session per product
    cache_key = f"viewed_{product.pk}_{session_key}"
    from django.core.cache import cache
    if not cache.get(cache_key):
        ProductView.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)
        cache.set(cache_key, True, 3600)
