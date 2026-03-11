from .models import WishlistItem

def wishlist_context(request):
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
        ids = list(WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        count = 0
        ids = []
    return {'wishlist_count': count, 'wishlist_product_ids': ids}
