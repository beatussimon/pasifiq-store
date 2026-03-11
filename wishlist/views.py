from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import WishlistItem
from products.models import Product

@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product').prefetch_related('product__images')
    return render(request, 'wishlist/list.html', {'wishlist_items': items})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        Product.objects.filter(pk=product_id).update(wishlist_count=product.wishlist_count - 1)
        action = 'removed'
    else:
        Product.objects.filter(pk=product_id).update(wishlist_count=product.wishlist_count + 1)
        action = 'added'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'action': action, 'count': WishlistItem.objects.filter(user=request.user).count()})
    
    messages.success(request, f'Product {action} {"to" if action == "added" else "from"} wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:list'))
