from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Setup initial store data - create owner account and sample categories'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create store owner
        if not User.objects.filter(username='owner').exists():
            user = User.objects.create_superuser(
                username='owner',
                email='owner@pasifiqstore.com',
                password='pasifiq2024',
                is_store_owner=True,
                first_name='Store',
                last_name='Owner'
            )
            self.stdout.write(self.style.SUCCESS('Created store owner: owner / pasifiq2024'))
        
        # Create sample categories
        from categories.models import Category
        sample_cats = [
            {'name': 'Electronics', 'description': 'Phones, laptops, and gadgets'},
            {'name': 'Fashion', 'description': 'Clothing, shoes, and accessories'},
            {'name': 'Home & Garden', 'description': 'Furniture and household items'},
            {'name': 'Sports', 'description': 'Sports equipment and outdoor gear'},
            {'name': 'Vehicles', 'description': 'Cars, motorcycles, and parts'},
            {'name': 'Collectibles', 'description': 'Rare and vintage Pacific items'},
        ]
        for cat_data in sample_cats:
            cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            if created:
                self.stdout.write(f'Created category: {cat.name}')
        
        # Create site settings
        from core.models import SiteSettings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                store_name='PASIFIQ STORE',
                tagline='Premium Pacific Products',
                phone='+679 123 4567',
                whatsapp='+6791234567',
                email='info@pasifiqstore.com',
                address='Pacific Islands',
                about_text='PASIFIQ STORE is your premier destination for quality Pacific products.',
            )
            self.stdout.write(self.style.SUCCESS('Created site settings'))
        
        # Create sample products
        from products.models import Product
        if not Product.objects.exists():
            for i, cat in enumerate(Category.objects.all()):
                Product.objects.create(
                    name=f"Sample {cat.name} Product",
                    category=cat,
                    description=f"This is a premium sample product for the {cat.name} category. Pacific inspired and quality guaranteed.",
                    short_description=f"A great {cat.name} item.",
                    price=(i + 1) * 99.99,
                    condition='new',
                    status='available',
                    is_featured=(i % 2 == 0),
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} sample products'))

        self.stdout.write(self.style.SUCCESS('\n✅ Store setup complete!\nLogin at /dashboard/ with: owner / pasifiq2024'))
