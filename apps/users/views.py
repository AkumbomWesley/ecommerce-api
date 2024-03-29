import traceback
from django.contrib.auth import authenticate, get_user_model, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .models import User
from permissions.custom_permissions import IsSuperUserOrAdminRole

User = get_user_model()
class UserCreateView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        print("Authenticated User:", user)

        if user is not None:
            login(request, user)
            try:
                refresh = RefreshToken.for_user(user)
                serializer = UserSerializer(user)
                response_data = {
                    'id': serializer.data.get('id'),
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                traceback_str = traceback.format_exc()
                print(f"Token creation error: {e}\n{traceback_str}")
                return Response({'error': 'Error creating tokens'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the token user ID matches the requested user ID
        if int(user_id) != request.user.id:
            return Response({'error': 'Invalid token for user ID'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the token user ID matches the requested user ID
        if int(user_id) != request.user.id:
            return Response({'error': 'Invalid token for user ID'}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DeleteAllUsersView(APIView):
    permission_classes = [IsSuperUserOrAdminRole]

    def delete(self, request, format=None):
        User.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)