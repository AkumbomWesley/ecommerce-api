from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data, role='customer')
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password','role',
                  'phone_number', 'gender', 'address', 'is_staff', 'is_admin', 'is_active',
                  'created_at', 'updated_at']

class CustomUserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number']
