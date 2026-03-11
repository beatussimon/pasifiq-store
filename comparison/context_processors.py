from .models import ComparisonItem

def comparison_context(request):
    if request.user.is_authenticated:
        items = ComparisonItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        items = ComparisonItem.objects.filter(session_key=session_key) if session_key else ComparisonItem.objects.none()
    
    return {
        'comparison_count': items.count(),
        'comparison_product_ids': list(items.values_list('product_id', flat=True)),
    }
