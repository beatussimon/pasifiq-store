from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Rating
from products.models import Product
from django.db.models import Avg

@login_required
def rate_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        score = int(request.POST.get('score', 0))
        review = request.POST.get('review', '')
        
        if 1 <= score <= 5:
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'score': score, 'review': review}
            )
            # Update product average
            avg = Rating.objects.filter(product=product).aggregate(avg=Avg('score'))['avg'] or 0
            count = Rating.objects.filter(product=product).count()
            Product.objects.filter(pk=product_id).update(average_rating=round(avg, 2), review_count=count)
            
            try:
                from notifications.utils import notify_owner_new_rating
                notify_owner_new_rating(rating)
            except:
                pass
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'score': score, 'average': float(avg), 'count': count, 'created': created})
            messages.success(request, 'Rating submitted successfully.')
        else:
            messages.error(request, 'Invalid rating score.')
    
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))
