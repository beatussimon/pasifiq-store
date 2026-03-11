from django.db import models
from django.conf import settings

class Message(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('archived', 'Archived'),
    ]

    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages')
    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL, related_name='inquiries')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status']), models.Index(fields=['-created_at'])]

    def __str__(self):
        return f"Message from {self.sender_name} - {self.created_at.strftime('%Y-%m-%d')}"

    def get_whatsapp_reply_url(self):
        import urllib.parse
        from django.conf import settings
        msg = f"Hi {self.sender_name}, thank you for your inquiry"
        if self.product:
            msg += f" about {self.product.name}"
        msg += "."
        phone = self.sender_phone.replace('+', '').replace(' ', '').replace('-', '')
        return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
