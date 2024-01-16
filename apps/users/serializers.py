from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
 
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}  # Set the role field as read-only
        }

class CustomUserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number']
