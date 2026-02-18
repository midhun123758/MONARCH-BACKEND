from rest_framework import serializers
from .models import CartItem

class CartitemSerializer(serializers.ModelSerializer):
    product_name=serializers.ReadOnlyField(source='product.name')
    product_img1=serializers.URLField(source='product.img1')
    product_price=serializers.ReadOnlyField(source='product.price')
    stock=serializers.ReadOnlyField(source='product.stock')
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=['id','product','product_name','product_price','subtotal','quantity','stock','product_img1']

    def get_subtotal(self,obj):
        return obj.product.price * obj.quantity