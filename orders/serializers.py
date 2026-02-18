from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Orders, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_stock = serializers.IntegerField(source="product.stock", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.img1", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'product_name',
            'quantity',
            'price',
            'product_stock',
            'product_image'
        ]
        read_only_fields = ['price']


class OrdersSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = [
            'id',
            'total_amount',          # fixed spelling
            'payment_status',        # new field
            'created_at',
            'items',
            'address'
        ]
        read_only_fields = [
            'total_amount',
            'payment_status'
        ]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        total_amount = Decimal("0.00")

        order = Orders.objects.create(
            user=user,
            address=validated_data.get('address'),
            payment_status="PENDING"
        )

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # 🔥 Stock validation
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}"
                )

            price = product.price
            total_amount += price * quantity

            # Reduce stock
            product.stock -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        order.total_amount = total_amount
        order.save()

        return order
