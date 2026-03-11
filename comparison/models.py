from django.db import models
from django.conf import settings

class ComparisonItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comparison_items', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    product = models.ForeignKey('products.Product', related_name='compared_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comparison_items'

    def __str__(self):
        return f"Compare: {self.product.name}"
