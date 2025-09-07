from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from eventapp.models import Event
from .models import Tier

from django.template.loader import render_to_string

# api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import TierSerializers

# Create your views here.

# admin






# -------------------------------------------- api ------------------------------------------------
@api_view(['POST'])
def api_add_tier(request):
    if request.method == 'POST':
        serializer = TierSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()  # create() in serializer handles stream lookup
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_view_tier(request):
    if request.method == 'GET':
        tiers = Tier.objects.select_related('event').all()                   # here 'event' is a forgeign key in the Tier model
        serializer = TierSerializers(tiers, many=True)
        return Response(serializer.data)
    
@api_view(['PUT','PATCH'])
def api_edit_tier(request , pk=None):
    try:
        tier = Tier.objects.get(id=pk)
    except Tier.DoesNotExist:
        return Response({'error': 'tier name not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TierSerializers(tier, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def api_delete_tier(request , pk):
    try:
        tier = Tier.objects.get(id=pk)
    except Tier.DoesNotExist:
        return Response({'error': 'tier name not found'}, status=status.HTTP_404_NOT_FOUND)
    
    tier.delete()
    return Response({'message': 'tier type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    



