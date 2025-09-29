
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from .models import Event
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





# Create your views here...............................................................
def add_events(request):
    if request.method == "POST":
        event_title = request.POST.get("event_title")
        description = request.POST.get("event_description")
        venue = request.POST.get("venue")
        location =request.POST.get("location")
        date = request.POST.get("myDate")
        time =request.POST.get("myTime")
        organizer =request.POST.get("organizer")
        banner =request.FILES.get("banner_image")   
        status=request.POST.get("status")
        print(event_title,description,venue,location,date,time)
        #   createdBy
        if event_title:
            #create event on db
            if not Event.objects.filter(title=event_title).exists():
                Event.objects.create(
                    title = event_title,
                    description = description,
                    venue=venue,
                    location = location,
                    date = date,
                    time = time,
                    organizer = organizer,
                    banner = banner,
                    status =status
                )

                events = Event.objects.all()
                html_data = render_to_string("partials/event_rows.html" , {"events":events})
                return JsonResponse({"events": html_data, "message": "Event saved successfully!"})

            else:
                return JsonResponse({"message": "Event with this name already exists."}, status=400)

        else:
            return JsonResponse({"message": "Cant be blank!!."}, status=400)


    return render(request , 'eventapp/add_event.html')

def view_events(request):
    events: QuerySet = Event.objects.all()
    return render(request, 'eventapp/add_event.html', {"events": events, "initial_load": True})

def edit_events(request , pk=None):
    event = get_object_or_404(Event , id=pk) if pk else None
    if request.method == "POST":
        event_title = request.POST.get("event_title")
        description = request.POST.get("event_description")
        venue = request.POST.get("venue")
        location =request.POST.get("location")
        date = request.POST.get("myDate")
        time =request.POST.get("myTime")
        organizer =request.POST.get("organizer")
        new_banner =request.FILES.get("banner_image")   # request.FILES.get("stream_image")
        status=request.POST.get("status")

        if event_title and description:
            # Exclude current event from duplicate check
              if not Event.objects.filter(title=event_title).exclude(pk=event.pk).exists():
                      # id: ObjectId, autocreated
                      #save to database
                        event.title=event_title
                        event.description = description
                        event.venue = venue
                        event.location = location
                        event.date = date
                        event.time = time 
                        event.organizer = organizer
                        event.status = status

                        if new_banner:
                             # Delete old image if exists
                            if event.banner and os.path.isfile(event.banner.path):
                                  os.remove(event.banner.path)

#                     # Assign new image
                        event.banner = new_banner
                        event.save()
                        
                        events = Event.objects.all()
                        html_data = render_to_string("partials/event_rows.html" , {"events":events})
                        return JsonResponse({"events": html_data, "message": "Event saved successfully!"})
              else:
                   return JsonResponse({"message": "Event with this name already exists."}, status=400)


             
        else:
             return JsonResponse({"message": "Cant be blank!!."}, status=400)


  









# _______________________________________ api _____________________________________________#

# @api_view(['POST'])
# def add_api_event(request):
#     serializer = EventSerializer(data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#         events = Event.objects.all()
#         all_events=EventSerializer(events , many=True).data
#         return Response({
#             'message':'events registrered successfully!!',
#             'events': all_events,
#         },status=status.HTTP_201_CREATED)
    
#     else:
#         return Response({
#             'message':'events registrered failed!!',
#             'error': serializer.errors,
#         },status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_api_event(request):
    events = Event.objects.all()
    all_events=EventSerializer(events , many=True,context={"request":request}).data
    if not all_events:
        return Response({"message": "No records found."}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"message": "List of all events",
            "events": all_events
        }, status=status.HTTP_200_OK)

      
# @api_view(['PUT', 'PATCH'])
# def edit_api_event(request,pk):
#      try:
#           event = Event.objects.get(id=pk)
#      except Event.DoesNotExist:
#           raise Response({"error":"Event not found."},status=status.HTTP_404_NOT_FOUND)
#      serializer = EventSerializer(instance=event , data=request.data , partial=(request.method == 'PATCH'))

#      if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data , status=status.HTTP_200_OK)
#      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# def delete_api_event(request,pk):
#     try :
#           event_info = Event.objects.get(id=pk)
#           event_info.delete()
#           return Response({"message": "Event deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#     except Event.DoesNotExist:
#          return Response({"message": "Event not found."}, status=status.HTTP_404_NOT_FOUND) 




# _______________________________________________ Class  Based View API __________________________________________________________________ #

# def view_events()
# no authentication & permission involved
class ReadAllEvent(ModelViewSet):
    queryset :QuerySet= Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = [
                    
                  'title',
                  'category__name',
                  'organization',
                  'location',
              
                  
                  ]


class EventViewSet(ModelViewSet):
    queryset :QuerySet= Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    #create a event 
    def perform_create(self ,serializer):
        user = self.request.user
        print("Inside perform_create -> ",user.first_name)
        if user.role != 'organizer':
            raise PermissionDenied("Only organizers can create events")
        
        # prevent duplicate event title
        title = serializer.validated_data.get('title')
        print(f"Creating event with title :{title} for user: {user}")

        if Event.objects.filter(title = title , organizer=user).exists():
            raise exceptions.ValidationError("Event with this title already exists for this admin")
        
        serializer.save(organizer=user)

    # view events created by each organizers
    @action(detail=False , methods=['get'],url_path='my-events' , permission_classes=[IsOrganizer])
    def my_events(self, request):
        user = request.user
        if user.role != 'organizer':
            raise PermissionDenied("Only you can see your own created events")
        
        all_events = Event.objects.filter(organizer=user)
        serializer = self.get_serializer(all_events,many=True)
        print(serializer)
        return Response(serializer.data)
    

    # View all events without any authentication
    @action(detail=False , methods=['get'],url_path='all-events' , permission_classes=[AllowAny] , authentication_classes=[])
    def all_events(self, request):
        all_events = Event.objects.all()
        serializer = self.get_serializer(all_events,many=True)
        print(serializer)
        return Response(serializer.data)




     # Edit an event - Only the organizer who created it
   
    def perform_update(self, serializer):
        event = self.get_object()   # This will get the course instance being updated from queryset = Course.objects.all() 
        user = self.request.user

        print(f"User details: {user}")

        if user.role != 'organizer' or event.organizer !=user:
            raise PermissionDenied("You can only update your own events.")
        serializer.save()


    
        # delete events
  
    def perform_destroy(self, instance):
        user = self.request.user
        print("-----------------for del--------------------------")
        print(user)
        print(instance)

        if instance.organizer != user:
            raise PermissionDenied("You can only delete remove their account.")

        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "event deleted successfully."}, 
            status=status.HTTP_200_OK
        )
    
    # popular events
    @action(detail=False , methods=['get'],url_path='popular-events' , permission_classes=[AllowAny] , authentication_classes=[])
    def popular_events(self, request):
        events = Event.objects.filter(is_popular=True)
        serializer = self.get_serializer(events,many=True)
        print(serializer)
        return Response(serializer.data)

    # @action(detail=False , methods=['get'],url_path='all-events-admin' , permission_classes=[AllowAny] , authentication_classes=[])
    # def all_events_admin(self, request):
    #     all_events = Event.objects.all()
    #     serializer = self.get_serializer(all_events,many=True)
    #     print(serializer)
    #     return Response(serializer.data)
    
    # @action(detail=False , methods=['Patch'],url_path='edit-by-admin' , permission_classes=[AllowAny] , authentication_classes=[])
    # def edit_by_admin(self, request):
    #     all_events = Event.objects.all()
    #     serializer = self.get_serializer(all_events,many=True)
    #     print(serializer)
    #     return Response(serializer.data)

