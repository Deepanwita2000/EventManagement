from django.shortcuts import render

# Create your views here.
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.db.models.query import QuerySet
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer

@api_view(['POST'])
@authentication_classes([])                 # disable authentication
@permission_classes([AllowAny])
def api_add_category(request):
    serializer: CategorySerializer = CategorySerializer(data = request.data , context={'request':request})    # Step 1: Deserializes the JSON data into Python native data types

    if serializer.is_valid():
        serializer.save()  # Step 2: Python native dict (after validation) and converts it into a Django model instance and then saves it.

        categories: QuerySet = Category.objects.all()
        all_categories: list[dict] = CategorySerializer(categories, many=True).data    # Step 3: Serializes converting QuerySet to Python native list of dictionaries.

        return Response({
            "message": "Category registered successfully!",
            "categories":  all_categories                                           # Step 4: Converts the list of dictionaries to JSON response
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "message": "Category registration failed!",    
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([])                 # disable authentication
@permission_classes([AllowAny])
def api_all_category(request):
    categories: QuerySet = Category.objects.all()  
    all_categories: list[dict] = CategorySerializer(categories, many=True , context={'request':request}).data

    if not all_categories:
        return Response({"message": "No categories found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "List of all categories",
            "categories": all_categories
        }, status=status.HTTP_200_OK)
