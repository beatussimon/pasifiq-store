from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('coming_soon', 'Coming Soon'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    category = models.ForeignKey('categories.Category', related_name='products', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    location = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    specifications = models.JSONField(default=dict, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Engagement metrics
    view_count = models.PositiveIntegerField(default=0)
    wishlist_count = models.PositiveIntegerField(default=0)
    comparison_count = models.PositiveIntegerField(default=0)
    inquiry_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['-view_count']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def is_available(self):
        return self.status == 'available'

    def get_whatsapp_url(self):
        from django.conf import settings
        import urllib.parse
        msg = f"Hi! I'm interested in: {self.name}"
        if self.price:
            msg += f" (TZS {int(self.price)})"
        # link = f"https://pasifiqstore.com{self.get_absolute_url()}"
        # Better: use a generic message without hardcoded domain if possible, or use a setting
        domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
        msg += f"\n\nProduct link: https://{domain}{self.get_absolute_url()}"
        return f"https://wa.me/{settings.STORE_WHATSAPP.replace('+','')}?text={urllib.parse.quote(msg)}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        ordering = ['-is_primary', 'sort_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.pk}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
