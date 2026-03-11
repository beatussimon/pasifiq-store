from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import SavedItem
from products.models import Product

@login_required
def saved_list(request):
    items = SavedItem.objects.filter(user=request.user).select_related('product').prefetch_related('product__images')
    return render(request, 'saved_items/list.html', {'saved_items': items})

@login_required
def toggle_saved(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = SavedItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        action = 'removed'
    else:
        action = 'saved'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'action': action})
    messages.success(request, f'Product {action}.')
    return redirect(request.META.get('HTTP_REFERER', 'saved_items:list'))
