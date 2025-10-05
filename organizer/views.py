from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string

from organizer.serializers import ProfileSerializer
from .models import MyProfile
from django.db.models.query import QuerySet
import os
# -----------------drf-------------------------
from rest_framework.decorators import api_view
from eventapp.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status



from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import filters

from django.utils import timezone
from datetime import timedelta

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import  User, UserToken

from accountapp.permission import IsOrganizerOrUser,IsOrganizer,IsUser,IsAdmin
from accountapp.serializers import UserSerializer


from eventapp.models import Event
from eventapp.serializers import EventSerializer

from django.db.models.query import QuerySet

# Create your views here.
class ProfileViewSet(ModelViewSet):
    queryset:QuerySet = MyProfile.objects.all()
    serializer_class=ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self ,serializer):
        user = self.request.user
        print("Inside perform_create -> ",user.first_name)
        if user.role != 'organizer':
            raise PermissionDenied("Only organizers can access profile")
        # print(serializer.data)
        # prevent duplicate event title
        # profile_id = serializer.data.get('gender')
        # print(f"Creating event with title :{profile_id},{profile_id.id} for user: {user}")

        if MyProfile.objects.filter(organizer=user).exists():
            raise exceptions.ValidationError("Account already exists")
        
        serializer.save(organizer=user)

    # Edit a course - Only the professor who created it
    def perform_update(self, serializer):
        myProfile = self.get_object()      # This will get the course instance being updated from queryset = Course.objects.all() 
        user = self.request.user

        print(f'User details: {user}')

        if user.role != 'organizer' or myProfile.organizer != user:
            raise PermissionDenied("You can only update your own profile.")
        serializer.save()

    @action(detail=False , methods=['get'],url_path='my-profile' , permission_classes=[IsOrganizer])
    def my_profile(self, request):
        user = request.user
        if user.role != 'organizer':
            raise PermissionDenied("Only you can see your own created events")
        # org_email = serializer.
        try:
             my_profile = MyProfile.objects.get(organizer=user)
        except MyProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=404)
        serializer = self.get_serializer(my_profile)
        print(serializer)
        return Response(serializer.data)

    





    
#  class EventViewSet(ModelViewSet):
#     queryset :QuerySet= Event.objects.all()
#     serializer_class = EventSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
  
#     #create a event 
#     def perform_create(self ,serializer):
#         user = self.request.user
#         print("Inside perform_create -> ",user.first_name)
#         if user.role != 'organizer':
#             raise PermissionDenied("Only organizers can create events")
        
#         # prevent duplicate event title
#         title = serializer.validated_data.get('title')
#         print(f"Creating event with title :{title} for user: {user}")

#         if Event.objects.filter(title = title , organizer=user).exists():
#             raise exceptions.ValidationError("Event with this title already exists for this admin")
        
#         serializer.save(organizer=user)

#     # view events created by each organizers
#     @action(detail=False , methods=['get'],url_path='my-events' , permission_classes=[IsOrganizer])
#     def my_events(self, request):
#         user = request.user
#         if user.role != 'organizer':
#             raise PermissionDenied("Only you can see your own created events")
        
#         all_events = Event.objects.filter(organizer=user)
#         serializer = self.get_serializer(all_events,many=True)
#         print(serializer)
#         return Response(serializer.data)
    

#     # View all events without any authentication
#     @action(detail=False , methods=['get'],url_path='all-events' , permission_classes=[AllowAny] , authentication_classes=[])
#     def all_events(self, request):
#         all_events = Event.objects.all()
#         serializer = self.get_serializer(all_events,many=True)
#         print(serializer)
#         return Response(serializer.data)




#      # Edit an event - Only the organizer who created it
   
#     def perform_update(self, serializer):
#         event = self.get_object()   # This will get the course instance being updated from queryset = Course.objects.all() 
#         user = self.request.user

#         print(f"User details: {user}")

#         if user.role != 'organizer' or event.organizer !=user:
#             raise PermissionDenied("You can only update your own events.")
#         serializer.save()


    
#         # delete events
  
#     def perform_destroy(self, instance):
#         user = self.request.user
#         print("-----------------for del--------------------------")
#         print(user)
#         print(instance)

#         if instance.organizer != user:
#             raise PermissionDenied("You can only delete remove their account.")

#         instance.delete()
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {"detail": "event deleted successfully."}, 
#             status=status.HTTP_200_OK
#         )
    
#     # popular events
#     @action(detail=False , methods=['get'],url_path='popular-events' , permission_classes=[AllowAny] , authentication_classes=[])
#     def popular_events(self, request):
#         events = Event.objects.filter(is_popular=True)
#         serializer = self.get_serializer(events,many=True)
#         print(serializer)
#         return Response(serializer.data)

#     # @action(detail=False , methods=['get'],url_path='all-events-admin' , permission_classes=[AllowAny] , authentication_classes=[])
#     # def all_events_admin(self, request):
#     #     all_events = Event.objects.all()
#     #     serializer = self.get_serializer(all_events,many=True)
#     #     print(serializer)
#     #     return Response(serializer.data)
    
#     # @action(detail=False , methods=['Patch'],url_path='edit-by-admin' , permission_classes=[AllowAny] , authentication_classes=[])
#     # def edit_by_admin(self, request):
#     #     all_events = Event.objects.all()
#     #     serializer = self.get_serializer(all_events,many=True)
#     #     print(serializer)
#     #     return Response(serializer.data)

