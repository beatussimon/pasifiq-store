from django import forms
from products.models import Product, ProductImage
from categories.models import Category
from core.models import SiteSettings

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'short_description', 'price', 'condition', 'status', 'tags', 'location', 'is_featured', 'is_active', 'meta_title', 'meta_description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
            'tags': forms.TextInput(attrs={'placeholder': 'electronics, mobile, samsung...'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', 'alt_text', 'is_primary')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'description', 'image', 'parent', 'is_active', 'sort_order')
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'about_text': forms.Textarea(attrs={'rows': 5}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
