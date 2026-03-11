from django.db import models
from django.conf import settings

class SavedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saved_items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='saved_by', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_items'
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"
