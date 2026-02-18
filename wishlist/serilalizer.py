# serializers.py
from rest_framework import serializers
from .models import Wishlist_item

class WishlistItemSerializer(serializers.ModelSerializer):
    
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.ReadOnlyField(source='product.img1') 

    class Meta:
        model = Wishlist_item
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image']
    