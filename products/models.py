from django.db import models
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    img1 = models.URLField(blank=True, null=True)
    img2 = models.URLField(blank=True, null=True)
    img3 = models.URLField(blank=True, null=True)
    img4 = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.name
