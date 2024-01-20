from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .serializers import StoreSerializer
from permissions.custom_permissions import IsStoreOwner, IsSuperUserOrAdminRole
from .models import Store

class StoreCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            user.role = 'owner'
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StoreDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({"Error": "Store Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoreUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsStoreOwner]

    def put(self, request, pk, format=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({"Error": "Store Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = StoreSerializer(store, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDeleteSingleView(APIView):
    permission_classes = [IsAuthenticated, IsStoreOwner]

    def delete(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({"Error": "Store Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        store.delete()
        return Response({"Message:" : "Store Deleted"}, status=status.HTTP_204_NO_CONTENT)

class StoreListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        products = Store.objects.all()
        serializer = StoreSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoreDeleteAllView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUserOrAdminRole]

    def delete(self, request):
        Store.objects.all().delete()
        return Response({"message":"All Stores Deleted"}, status=status.HTTP_204_NO_CONTENT)