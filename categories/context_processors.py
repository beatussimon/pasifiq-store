from .models import Category


def categories_nav(request):
    try:
        categories = Category.objects.filter(
            parent=None, is_active=True
        ).prefetch_related('children')[:10]
    except Exception:
        categories = []
    return {'nav_categories': categories}
