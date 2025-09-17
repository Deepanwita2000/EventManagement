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


from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.utils import timezone
from datetime import timedelta

from accountapp.authentication import JWTAuthentication

from accountapp.permission import IsOrganizer




# Create your views here.

# admin






# -------------------------------------------- api ------------------------------------------------
# @api_view(['POST'])
# def api_add_tier(request):
#     if request.method == 'POST':
#         serializer = TierSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # create() in serializer handles stream lookup
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def api_view_tier(request):
#     if request.method == 'GET':
#         tiers = Tier.objects.select_related('event').all()                   # here 'event' is a forgeign key in the Tier model
#         serializer = TierSerializers(tiers, many=True)
#         return Response(serializer.data)
    
# @api_view(['PUT','PATCH'])
# def api_edit_tier(request , pk=None):
#     try:
#         tier = Tier.objects.get(id=pk)
#     except Tier.DoesNotExist:
#         return Response({'error': 'tier name not found'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = TierSerializers(tier, data=request.data, partial=(request.method == 'PATCH'))
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['DELETE'])
# def api_delete_tier(request , pk):
#     try:
#         tier = Tier.objects.get(id=pk)
#     except Tier.DoesNotExist:
#         return Response({'error': 'tier name not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     tier.delete()
#     return Response({'message': 'tier type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class TierViewSet(ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #create ticket tier:
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'organizer':        # Only organizer can create
            raise PermissionDenied("Only organizer can create ticket.")
        # Prevent duplicate course
        title = serializer.validated_data.get('event_title')
        print(f'Creating course with title: {title} for user: {user}')
        event=Event.objects.get(title=title)

        if Tier.objects.filter(event=event.id , organizer=user).exists():
            raise exceptions.ValidationError("organizer with this event is already registered.")
        serializer.save(organizer=user)
  
    # List events created by the specific authenticated organizer
    @action(detail=False, methods=['get'], url_path='my-tickets', permission_classes=[IsOrganizer])
    def my_tickets(self, request):
        user = request.user
        if user.role != 'organizer':
            raise PermissionDenied("Only organizer can access their own events.")

        tiers = Tier.objects.filter(organizer=user)
        serializer = self.get_serializer(tiers, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        tier = self.get_object()      # This will get the course instance being updated from queryset = Tier.objects.all() 
        user = self.request.user

        print(f'User details: {user}')

        if user.role != 'organizer' or tier.organizer !=user:
            raise PermissionDenied("only organizer can update it's own events.")
        serializer.save()
        

    # delete event
    def perform_destroy(self, instance):
        user = self.request.user
        print("-----------------for del--------------------------")
        print(user)
        print(instance)

        if instance.organizer != user:
            raise PermissionDenied("You can only delete remove your own ticket info.")

        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "ticket info deleted successfully."}, 
            status=status.HTTP_200_OK
        )

      