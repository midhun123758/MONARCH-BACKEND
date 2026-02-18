from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.
class Wishlist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}'s wishlist"
    
class Wishlist_item(models.Model):
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE ,related_name= 'product')
    added_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
      constraints = [
        models.UniqueConstraint(
            fields=['wishlist', 'product'],
            name='unique_product_per_wishlist'
        )
    ]
    def __str__(self):
        return f"{self.product.name}"
    