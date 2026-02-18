from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,UserSerializer,sendOTpSerilaizer,ResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import random
from .models import createPassword
from django.core.mail import send_mail
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]  # ✅ spelling fixed
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthMe(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data)
    

class sendotpView(APIView):
    def post(self,request):
        serialiser=sendOTpSerilaizer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        
        email=serialiser.validated_data['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response ({"error": "Email not registered"}, status=400)

        otp = str(random.randint(100000, 999999))
        createPassword.objects.filter(user=user).delete()

        createPassword.objects.create(
            user=user,
            otp=otp
        )

        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}. Valid for 5 minutes.",
            "noreply@example.com",
            [email],
        )

        return Response({"message": "OTP sent successfully"}, status=200)
    
from datetime import timedelta
from django.utils import timezone

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj = createPassword.objects.get(user=user, otp=otp)
        except:
            return Response({"error": "Invalid OTP"}, status=400)

        if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
            otp_obj.delete()
            return Response({"error": "OTP expired"}, status=400)

        otp_obj.is_verified = True
        otp_obj.save()

        return Response({"message": "OTP verified"})


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            otp_obj = createPassword.objects.get(user=user, is_verified=True)
        except:
            return Response({"error": "OTP not verified"}, status=400)

        user.set_password(new_password)
        user.save()

        otp_obj.delete()

        return Response({"message": "Password reset successful"})
