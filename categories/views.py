from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product

def category_list(request):
    categories = Category.objects.filter(is_active=True, parent=None).prefetch_related('children', 'products')
    return render(request, 'categories/list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    subcategories = category.children.filter(is_active=True)
    products = Product.objects.filter(category=category, is_active=True).prefetch_related('images')
    
    # Filter
    condition = request.GET.get('condition')
    sort = request.GET.get('sort', '-created_at')
    
    if condition:
        products = products.filter(condition=condition)
    
    valid_sorts = {'-created_at': '-created_at', 'view_count': '-view_count', 'price': 'price', '-price': '-price', 'name': 'name'}
    products = products.order_by(valid_sorts.get(sort, '-created_at'))
    
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'categories/detail.html', {
        'category': category,
        'subcategories': subcategories,
        'products': page,
        'condition': condition,
        'sort': sort,
    })
