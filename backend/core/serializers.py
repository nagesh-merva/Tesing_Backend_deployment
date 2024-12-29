from rest_framework import serializers
from .models import Image, ServiceImage
from .models import CustomUser

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'description', 'type']



class ServiceImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = ServiceImage
        fields = ['id', 'icon', 'service', 'feature']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['is_active']  # Prevent non-admins from modifying this field


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }