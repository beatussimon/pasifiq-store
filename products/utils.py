from django.db.models import Q
from .models import Product

def get_filtered_products(request, queryset=None):
    if queryset is None:
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    # Text Search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(location__icontains=search_query)
        ).distinct()

    # Category
    category_slug = request.GET.get('category')
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    # Condition
    condition = request.GET.get('condition')
    if condition:
        queryset = queryset.filter(condition=condition)
        
    # Status
    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)
        
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        '-created_at': '-created_at',
        'newest': '-created_at',
        'view_count': '-view_count',
        'popular': '-view_count',
        'rating': '-average_rating',
        'rated': '-average_rating',
        'price_asc': 'price',
        'price': 'price',
        'price_desc': '-price',
        '-price': '-price',
        'name': 'name',
        'wishlist': '-wishlist_count',
    }
    queryset = queryset.order_by(valid_sorts.get(sort, '-created_at'))
    
    return queryset
