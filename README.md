# 🌊 PASIFIQ STORE

A premium showcase commerce platform built with Django — Pacific-inspired design with powerful management tools.

## Features

### Customer Features
- 🛍️ Browse products with advanced filtering & sorting
- 🔍 Full-text search with instant suggestions
- ❤️ Wishlist management
- 🔖 Saved items
- ⚖️ Product comparison (up to 4 items)
- ⭐ Product ratings & reviews
- 📞 Contact via Phone, WhatsApp, or internal messaging
- 👤 User accounts with profile management

### Owner Dashboard
- 📦 Product management (create, edit, delete, feature)
- 🖼️ Multi-image upload per product
- 📁 Category management
- 📬 Message inbox with WhatsApp/phone reply
- 📊 Analytics with charts
- 👥 User overview
- ⚙️ Store settings

### Technical
- Django 4.2+ with SQLite (PostgreSQL-ready)
- Responsive mobile-first design
- SEO-optimized (sitemap, meta tags, robots.txt)
- Image lazy loading
- Session-based comparison for guests
- Notification system for owners
- CSRF & XSS protection

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations core categories products wishlist saved_items comparison ratings messaging analytics notifications
python manage.py migrate
```

### 3. Setup store (creates owner account + sample data)
```bash
python manage.py setup_store
```

### 4. Run development server
```bash
python manage.py runserver
```

### 5. Access
- **Store:** http://localhost:8000/
- **Dashboard:** http://localhost:8000/dashboard/
- **Admin:** http://localhost:8000/admin/

**Default credentials:** `owner` / `pasifiq2024`

## Configuration

Copy `.env.example` to `.env` and update:
```env
SECRET_KEY=your-secret-key
STORE_PHONE=+1234567890
STORE_WHATSAPP=+1234567890
STORE_EMAIL=info@yourstore.com
```

## Production Deployment

```bash
# Collect static files
python manage.py collectstatic

# Use gunicorn
gunicorn pasifiq_store.wsgi:application --bind 0.0.0.0:8000
```

Set `DEBUG=False` and configure a proper `SECRET_KEY` in production.

## Project Structure

```
pasifiq_store/
├── pasifiq_store/     # Django project config
├── core/              # Home, About, Contact pages + site settings
├── users/             # Custom user model + authentication
├── products/          # Product catalog + detail pages
├── categories/        # Category hierarchy
├── wishlist/          # Wishlist system
├── saved_items/       # Saved/bookmarked products
├── comparison/        # Product comparison
├── ratings/           # Star ratings & reviews
├── messaging/         # Contact & inquiry system
├── analytics/         # View tracking & stats
├── notifications/     # Owner notification system
├── dashboard/         # Owner management dashboard
├── search_app/        # Search + suggestions
├── templates/         # All HTML templates
├── static/            # CSS, JS, images
│   ├── css/main.css
│   ├── css/dashboard.css
│   └── js/main.js
└── media/             # User-uploaded files (auto-created)
```

## Extending

### Add online payments
Install `stripe` and add a `payments` app. Update `Product.status` flow.

### Add inventory tracking
Add `stock` field to `Product` and decrease on sale.

### Add multi-vendor
Add `Vendor` model linked to `CustomUser`, attach to `Product`.
