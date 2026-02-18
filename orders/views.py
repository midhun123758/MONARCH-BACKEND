import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Orders
from .serializers import OrdersSerializer
from cart.models import CartItem

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            payment_method = request.data.get("payment_method", "razorpay")

            serializer = OrdersSerializer(
                data=request.data,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            order = serializer.save()
            if payment_method.lower() == "cod":
                order.payment_status = "PENDING"
                order.save()

         
                CartItem.objects.filter(
                    cart__user=request.user,
                    product__in=order.items.values_list("product_id", flat=True)
                ).delete()

                return Response({
                    "message": "Order placed successfully (COD)",
                    "db_order_id": order.id
                }, status=status.HTTP_201_CREATED)

            razorpay_order = client.order.create({
                "amount": int(order.total_amount * 100),  # Convert to paise
                "currency": "INR",
                "payment_capture": "1"
            })
            order.razorpay_order_id = razorpay_order.get("id")
            order.save()

            return Response({
                "db_order_id": order.id,
                "razorpay_order_id": razorpay_order.get("id"),
                "amount": razorpay_order.get("amount"),
                "currency": razorpay_order.get("currency"),
                "key": settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            # Required params
            db_order_id = request.data.get("db_order_id")
            razorpay_order_id = request.data.get("razorpay_order_id")
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_signature = request.data.get("razorpay_signature")

            # Validate input
            if not all([db_order_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response(
                    {"error": "All payment parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }

            # Verify Razorpay Signature
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return Response(
                    {"error": "Invalid payment signature"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the order
            try:
                order = Orders.objects.get(id=db_order_id, user=request.user)
            except Orders.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            # Update order status
            order.payment_status = "SUCCESS"
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()

            # Remove ordered products from cart
            CartItem.objects.filter(
                cart__user=request.user,
                product__in=order.items.values_list("product_id", flat=True)
            ).delete()

            return Response({"status": "Payment Successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            orders = Orders.objects.filter(user=request.user).order_by('-created_at')
            serializer = OrdersSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
