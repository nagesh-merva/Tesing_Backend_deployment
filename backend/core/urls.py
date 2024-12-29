from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import  ForgotPasswordView, ImageViewSet, ResetPasswordView, ServiceImageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='image')
router.register(r'service-images', ServiceImageViewSet, basename='service-image')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path('', include(router.urls)),
]
