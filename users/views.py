from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm

def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import login
            login(request, user)
            messages.success(request, f'Welcome to PASIFIQ STORE, {user.username}!')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    from wishlist.models import WishlistItem
    from saved_items.models import SavedItem
    from messaging.models import Message
    from ratings.models import Rating
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product').prefetch_related('product__images')[:6]
    saved = SavedItem.objects.filter(user=request.user).select_related('product').prefetch_related('product__images')[:6]
    inquiries = Message.objects.filter(user=request.user).order_by('-created_at')[:5]
    ratings = Rating.objects.filter(user=request.user).select_related('product')[:5]
    return render(request, 'users/profile.html', {
        'wishlist_items': wishlist_items,
        'saved_items': saved,
        'inquiries': inquiries,
        'ratings': ratings,
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})
