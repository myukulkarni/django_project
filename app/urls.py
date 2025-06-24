from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, PublicView, ProtectedView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/<int:user_id>/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
     path('public/', PublicView.as_view(), name='public-endpoint'),
    path('protected/', ProtectedView.as_view(), name='protected-endpoint'),
]
