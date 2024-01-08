from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserCreateView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        # Your login logic goes here
        # ...

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            self.check_object_permissions(self.request, user)  # Check object-level permissions
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetAllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, format=None):
        user = self.get_object(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            self.check_object_permissions(self.request, user)  # Check object-level permissions
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteAllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, format=None):
        User.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)