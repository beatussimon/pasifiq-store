from django.conf import settings
from .models import SiteSettings

def global_context(request):
    try:
        site_settings = SiteSettings.objects.first()
    except:
        site_settings = None

    return {
        'store_name': getattr(site_settings, 'store_name', settings.STORE_NAME),
        'store_phone': getattr(site_settings, 'phone', settings.STORE_PHONE),
        'store_whatsapp': getattr(site_settings, 'whatsapp', settings.STORE_WHATSAPP),
        'store_email': getattr(site_settings, 'email', settings.STORE_EMAIL),
        'store_address': getattr(site_settings, 'address', settings.STORE_ADDRESS),
        'site_settings': site_settings,
    }
