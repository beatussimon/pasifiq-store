from django import template
from categories.models import Category

register = template.Library()

@register.simple_tag
def get_nav_categories():
    return Category.objects.filter(is_active=True, parent=None)[:8]

@register.filter
def stars_range(value):
    try:
        return range(1, 6)
    except:
        return range(1, 6)

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except:
        return 0

@register.filter
def percentage(value, total):
    try:
        if total == 0:
            return 0
        return round((value / total) * 100)
    except:
        return 0

@register.filter
def get_dict_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None
