from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from accountapp.authentication import JWTAuthentication
from accountapp.models import User
from accountapp.permission import IsUser
from eventapp.models import Event
from booking.models import Booking
from django.template.loader import render_to_string

from rest_framework.decorators import api_view
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

from .serializers import BookSerializer


# class AllBookingsView(ModelViewSet):
#     queryset = Booking.objects.all()             # This will be used for listing and retrieving courses
#     serializer_class = BookSerializer
#     authentication_classes = []
#     permission_classes = []
#     filter_backends = [filters.SearchFilter]
#     search_fields = [
#                  ''                               
#                   ]


# serializer.validated_data.get('event_title')
# Create your views here.
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()             # This will be used for listing and retrieving courses
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[IsUser])
    def book_ticket(self,serializer):
        user = self.request.user   
        print(serializer.validated_data)       # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        if user.role != 'user':        # Only professors can create
            raise PermissionDenied("Only User can book tickets.")
        # Booking.objects.create(user=user)
        # return Response({'detail': 'Enrolled successfully'})

    @action(detail=False , methods=['get'],url_path='my-bookings' , permission_classes=[IsUser])
    def my_bookings(self,request):
        user = request.user
        if user.role != 'user':
            raise PermissionDenied("Only user can see booking details")
        bookings=Booking.objects.filter(user=user)
        serializer = self.get_serializer(bookings,many=True)
        print(serializer)
        return Response(serializer.data)


    #         @action(detail=False , methods=['get'],url_path='my-events' , permission_classes=[IsOrganizer])
    # def my_events(self, request):
    #     user = request.user
    #     if user.role != 'organizer':
    #         raise PermissionDenied("Only you can see your own created events")
        
    #     all_events = Event.objects.filter(organizer=user)
    #     serializer = self.get_serializer(all_events,many=True)
    #     print(serializer)
    #     return Response(serializer.data)
   
  
