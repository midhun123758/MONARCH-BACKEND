from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Wishlist, Wishlist_item
from products.models import Product
from .serilalizer import WishlistItemSerializer

class AddToWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist_item = Wishlist_item.objects.filter(wishlist=wishlist, product=product).first()

        
        if wishlist_item:
            wishlist_item.delete()
            return Response(
                {"message": "Removed from wishlist", "product_id": product_id}, 
                status=status.HTTP_200_OK
            )

        wishlist_item = Wishlist_item.objects.create(wishlist=wishlist, product=product)
        serializer = WishlistItemSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        items = wishlist.items.select_related("product").all() # Added .all()
        serializer = WishlistItemSerializer(items, many=True)
        return Response({"wishlist_items": serializer.data})

class DeleteWishlistItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = Wishlist_item.objects.get(id=item_id, wishlist__user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wishlist_item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)