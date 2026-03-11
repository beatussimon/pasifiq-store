from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import ComparisonItem
from products.models import Product

def _get_comparison_items(request):
    if request.user.is_authenticated:
        return ComparisonItem.objects.filter(user=request.user).select_related('product').prefetch_related('product__images')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return ComparisonItem.objects.filter(session_key=session_key).select_related('product').prefetch_related('product__images')

def comparison_view(request):
    items = _get_comparison_items(request)
    products = [item.product for item in items]
    
    # Gather all spec keys
    all_specs = set()
    for p in products:
        all_specs.update(p.specifications.keys())
    
    return render(request, 'comparison/view.html', {
        'comparison_products': products,
        'all_specs': sorted(all_specs),
    })

def add_to_comparison(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    items = _get_comparison_items(request)
    
    limit = getattr(settings, 'COMPARISON_LIMIT', 4)
    if items.count() >= limit:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': f'Maximum {limit} products for comparison.'}, status=400)
        messages.warning(request, f'Maximum {limit} products can be compared at once.')
        return redirect(request.META.get('HTTP_REFERER', 'comparison:view'))
    
    if request.user.is_authenticated:
        ComparisonItem.objects.get_or_create(user=request.user, product=product)
    else:
        session_key = request.session.session_key or request.session.create() or request.session.session_key
        ComparisonItem.objects.get_or_create(session_key=session_key, product=product)
    
    Product.objects.filter(pk=product_id).update(comparison_count=product.comparison_count + 1)
    
    new_count = _get_comparison_items(request).count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'action': 'added', 'count': new_count})
    messages.success(request, f'{product.name} added to comparison.')
    return redirect(request.META.get('HTTP_REFERER', 'comparison:view'))

def remove_from_comparison(request, product_id):
    if request.user.is_authenticated:
        ComparisonItem.objects.filter(user=request.user, product_id=product_id).delete()
    else:
        session_key = request.session.session_key
        if session_key:
            ComparisonItem.objects.filter(session_key=session_key, product_id=product_id).delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = _get_comparison_items(request).count()
        return JsonResponse({'action': 'removed', 'count': count})
    return redirect('comparison:view')

def clear_comparison(request):
    if request.user.is_authenticated:
        ComparisonItem.objects.filter(user=request.user).delete()
    else:
        session_key = request.session.session_key
        if session_key:
            ComparisonItem.objects.filter(session_key=session_key).delete()
    return redirect('comparison:view')
