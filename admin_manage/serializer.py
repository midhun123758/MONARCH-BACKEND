from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Orders
class UsermanageSerilaizer(serializers.ModelSerializer):
    class Meta :
        model=User
        fields='__all__'


class ProductmanageSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= '__all__'


class orderserilaizer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields='__all__'

    