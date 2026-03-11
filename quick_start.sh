#!/bin/bash
echo "=== PASIFIQ STORE Quick Start ==="

# Check Django
python3 -c "import django" 2>/dev/null || { echo "Install: pip install -r requirements.txt"; exit 1; }

# Migrations
echo "Running migrations..."
python3 manage.py makemigrations users 2>&1 | tail -1
python3 manage.py makemigrations core categories products wishlist saved_items comparison ratings messaging analytics notifications 2>&1 | tail -1
python3 manage.py migrate 2>&1 | tail -3

# Setup store
echo "Setting up store..."
python3 manage.py setup_store

echo ""
echo "=== Starting server ==="
echo "Store: http://localhost:8000/"
echo "Dashboard: http://localhost:8000/dashboard/"
echo "Login: owner / pasifiq2024"
echo ""
python3 manage.py runserver
