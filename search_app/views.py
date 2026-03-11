from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from products.models import Product
from categories.models import Category

from products.utils import get_filtered_products

def search(request):
    products = get_filtered_products(request)
    query = request.GET.get('q', '').strip()

    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'search_app/results.html', {
        'query': query,
        'products': page,
        'result_count': products.count() if query else 0,
        'condition': request.GET.get('condition', ''),
        'sort': request.GET.get('sort', 'relevance'),
    })

def search_suggestions(request):
    from django.urls import reverse
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(name__icontains=query, is_active=True).values('name', 'slug')[:5]
        results = [{'name': p['name'], 'url': reverse('products:detail', kwargs={'slug': p['slug']})} for p in products]
    return JsonResponse({'suggestions': results})
