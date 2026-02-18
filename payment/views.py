import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import CreateOrderSerializer,VerifyPaymentSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Razorpay needs amount in paise
        amount = serializer.validated_data['amount'] * 100  

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        Order.objects.create(
            user=request.user,
            amount=amount,
            razorpay_order_id=razorpay_order['id'],
            is_paid=False
        )

        return Response({
            "order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount
        })
class VerifyPaymentView(APIView):

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })

            order = Order.objects.get(
                razorpay_order_id=data["razorpay_order_id"]
            )

            if order.is_paid:
                return Response({"message": "Order already paid"})

            order.is_paid = True
            order.save()

            return Response({"message": "Payment successful"})

        except Exception:
            return Response(
                {"error": "Payment verification failed"},
                status=400
            )
