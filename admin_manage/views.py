from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
import razorpay

from orders.models import Orders, Revenue
from products.models import Product
from .serializer import UsermanageSerilaizer, ProductmanageSerilaizer, orderserilaizer


# ---------------- USERS ----------------
class AllUserView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UsermanageSerilaizer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UsermanageSerilaizer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditUserView(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UsermanageSerilaizer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------- PRODUCTS ----------------
class AllProducts(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(is_deleted=False)
            serializer = ProductmanageSerilaizer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsingleView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk, is_deleted= False)
            serializer = ProductmanageSerilaizer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddproductView(APIView):
    def post(self, request):
        try:
            serializer = ProductmanageSerilaizer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditProductView(APIView):
    def patch(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductmanageSerilaizer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def soft_delete_view(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.is_deleted = True
        product.save()
        return Response({"message": "Product soft deleted successfully"})
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------- ORDERS ----------------
class AllOrders(APIView):
    def get(self, request):
        try:
            orders = Orders.objects.all()
            serializer = orderserilaizer(orders, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateOrderStatusView(APIView):
    def patch(self, request, pk):
        try:
            order = Orders.objects.get(id=pk)
            new_status = request.data.get("payment_status")
            if not new_status:
                return Response({"error": "payment_status is required"}, status=status.HTTP_400_BAD_REQUEST)

            order.payment_status = new_status
            order.save()

            return Response({
                "message": "Order status updated successfully",
                "new_status": order.payment_status
            })
        except Orders.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------- REVENUE ----------------
class DashboardRevenueView(APIView):
    def get(self, request):
        try:
            revenue = Revenue.objects.first()
            total = revenue.total_revenue if revenue else 0
            return Response({"total_revenue": total})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------- RAZORPAY PAYMENT ----------------
@api_view(['POST'])
def Create_payment(request):
    try:
        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            "amount": int(amount) * 100,  # Razorpay works in paise
            "currency": "INR",
            "payment_capture": "1"
        })
        return Response(order)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
