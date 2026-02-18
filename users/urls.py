from django.urls import path
from .views import RegisterView, LoginView, LogoutView,AuthMe, ResetPasswordView, VerifyOTPView,sendotpView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path("auth/me/", AuthMe.as_view(), name="me"),
    path('forgot-password/', sendotpView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),


]