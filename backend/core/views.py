
from rest_framework.viewsets import ModelViewSet

from backend.settings import EMAIL_HOST_USER
from .models import Image, ServiceImage
from .serializers import ImageSerializer, ServiceImageSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .serializers import UserSerializer, UserUpdateSerializer
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache



#comment to test changesin github


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ServiceImageViewSet(ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'list', 'partial_update']:
            return [IsAdminUser()]
        elif self.action in ['update']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        user = self.get_object()

       
        if user != request.user and not request.user.is_staff:
            return Response({'detail': 'You are not allowed to update this user.'}, status=status.HTTP_403_FORBIDDEN)

       
        if 'password' in request.data:
            password = request.data.pop('password')
            user.password = make_password(password)

       
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)




class ForgotPasswordView(APIView):
    def post(self, request):
        username = request.data.get("username")
        try:
            user = CustomUser.objects.get(username=username)
            verification_code = f"{random.randint(100000, 999999)}"
            
            # Store the code in the cache for 10 minutes
            cache.set(f"verification_code_{user.id}", verification_code, timeout=600)
            
            # Email content
            subject = "Password Reset Verification Code"
            message = f"Hello {user.username},\n\nYour password reset verification code is: {verification_code}\n\nThis code is valid for 10 minutes."
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "Verification code sent to your email."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        try:
            user = CustomUser.objects.get(username=username)
            # Retrieve the code from the cache
            cached_code = cache.get(f"verification_code_{user.id}")
            if cached_code != code:
                return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Delete the code from the cache
            cache.delete(f"verification_code_{user.id}")
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)