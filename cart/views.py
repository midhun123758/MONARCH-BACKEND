from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart,CartItem
from products.models import Product
from .serializer import CartitemSerializer
from rest_framework import status
class Addtocart(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=int(request.data.get('quantity',1))
        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product=Product.objects.get(id=product_id)
            product_stock=product.stock
        except Product.DoesNotExist:
            return Response(
                   {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        if not created:
           new_quantity = cart_item.quantity + quantity
           if new_quantity > product.stock:

            return Response(
                {"error": "Quantity exceeds available stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
           cart_item.quantity = new_quantity
        else:
            if quantity > product.stock:
               return Response(
                {"error": "Quantity exceeds available stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
            cart_item.quantity = quantity

        cart_item.save()

        serializer = CartitemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserCartview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({
                "cart_items": [],
                "total_price": 0
            })
        items = cart.items.all().order_by('id') 
        serializer = CartitemSerializer(items, many=True)

        total=sum([item.quantity * item.product.price for item in items])
        return Response({
            "cart_items": serializer.data,
            "total_price": total
        })
    
class DeleteCart(APIView):
    def delete(self,request,item_id):
        try:
            product=CartItem.objects.get(id=item_id,cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error":"item not found"},status=status.HTTP_404_NOT_FOUND)
        product.delete()

        return  Response({ "message":"item removed from cart"},status=status.HTTP_204_NO_CONTENT)
    
class UpdateCart(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,item_id):
        try:
            cart_item=CartItem.objects.get(id=item_id,cart__user=request.user)
        except CartItem .DoesNotExist:
            return Response({"Error":'item not Found'},status=status.HTTP_404_NOT_FOUND)
           
        quantity=request.data.get("quantity")

        if quantity is None or int(quantity)<=0:
            return Response({"error": " quantity must be grater than 0"},status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity=quantity
        cart_item.save()
        return Response({
            "message ":"cart item updated",
            "item_id":cart_item.id,
            "quantity":cart_item.quantity
        },status=status.HTTP_200_OK)
    

    