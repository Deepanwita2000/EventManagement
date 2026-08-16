
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
# from .models import Event
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
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import filters

from django.utils import timezone
from datetime import timedelta

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import  User, UserToken

from accountapp.permission import IsOrganizerOrUser,IsOrganizer,IsUser,IsAdmin
from accountapp.serializers import UserSerializer


from eventapp.models import Event, LandscapeImage, PortraitImage
from eventapp.serializers import EventSerializer

from django.db.models.query import QuerySet

from accountapp.models import MyProfile

from .models import Category, Event

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
from django.db import transaction
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


class BaseClass(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  

class CreateEventViewSet(BaseClass):
    """
    payload :form-data
    {
    "title": "string",
    "description": "string",
    "location": "string",
    "venue": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "duration": "string",
    "languages": [
        "string"
    ],
    "age": "string",
    "organization": "string",
    "is_popular": true,
    "status": "active",
    "category": 1,
    "landscapes": [
        "image_file_1",
        "image_file_2"
    ],
    "portraits": [
        "image_file_1",
        "image_file_2"
    ]
}
    """
    queryset = Event.objects.select_related("created_by","updated_by","category").all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        print("Request data:", self.request.data)
        print("Validated data:", serializer.validated_data)
        # landscapes = self.request.FILES.getlist("landscapes")
        # portraits = self.request.FILES.getlist("portraits")

        with transaction.atomic():

            user = self.request.user

            if user.role != "organizer":
                raise PermissionDenied("Only organizers can create events.")
     
            title = serializer.validated_data["title"]
            if Event.objects.filter(title=title,created_by=user).exists():
                raise exceptions.ValidationError({"title": "You have already created an event with this title."})

            event=serializer.save(created_by=user,updated_by=user)
            for image in self.request.FILES.getlist("landscapes"):
                LandscapeImage.objects.create(event=event,image=image,created_by=user,updated_by=user)

            for image in self.request.FILES.getlist("portraits"):
                PortraitImage.objects.create(event=event, image=image, created_by=user, updated_by=user,)
            
    def perform_update(self, serializer):
        with transaction.atomic():
            user = self.request.user

            event = self.get_object()

            # Allow only the creator to update
            if event.created_by != user:
                raise PermissionDenied("You cannot update this event.")

            event = serializer.save(updated_by=user)

            # Optional: Replace landscape images
            landscapes = self.request.FILES.getlist("landscapes")
            if landscapes:
                event.landscapes.all().delete()

                for image in landscapes:
                    LandscapeImage.objects.create(
                        event=event,
                        image=image,
                        created_by=user,
                        updated_by=user,
                    )

            # Optional: Replace portrait images
            portraits = self.request.FILES.getlist("portraits")
            if portraits:
                event.portraits.all().delete()

                for image in portraits:
                    PortraitImage.objects.create(
                        event=event,
                        image=image,
                        created_by=user,
                        updated_by=user,
                    )

    def perform_delete(Self,serializer):...



from django.db.models import Q


class FilterEvents(ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def list(self, request):

        city = request.GET.get("city")
        category = request.GET.get("category")

        events = Event.objects.filter(
            is_active=True,
            status="active"
        )

        if city:
            events = events.filter(
                location__icontains=city
            )

        if category:
            events = events.filter(
                category__name__icontains=category
            )

        serializer = EventSerializer(events, many=True)

        data = []

        for event in serializer.data:

            data.append({
                "title": event["title"],
                "category_name": event["category_name"],
                "portrait": event["portraits"][0]["image"] if event["portraits"] else None,
                "landscape": event["landscapes"][0]["image"] if event["landscapes"] else None,
                "venue": event["venue"],
                "date": event["date"],
                "time": event["time"],
            })

        return Response(
            {
                "count": events.count(),
                "data": data
            }
        )









class AllEvents(ViewSet):
    """
    {"event_id":11}
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def list(self,request):
        print("hello")
        all_events= Event.objects.all()
        serializer= EventSerializer(all_events , many=True)
        return Response({
            "data":serializer.data
        })
    def create(self,request):
        print(request.data)
        event_id = request.data.get("event_id")
        event=Event.objects.get(id=event_id)
        serializer=EventSerializer(event)
        # serializer.data.pop("status")
        return Response({
            "data":serializer.data
        })


    # "status": "active",
    #     "is_popular": false,
    #     "created_by": "susmita@gmail.com",
    #     "updated_by": "susmita@gmail.com"

# class 







# using full-text search here
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class CustomSearch(ViewSet):
    """
    search for these fields :
            "title",
            "description",
            "venue",
            "location",
            "organization"
        )
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def list(self, request):
        search = request.GET.get("search", "").strip()
        print(search)

        if not search:
            return Response(
                {
                    "message": "Please provide a search keyword."
                },
                status=400
            )

        vector = SearchVector(
            "title",
            "description",
            "venue",
            "location",
            "organization"
        )

        query = SearchQuery(search)

        # events = (
        #     Event.objects.filter(
        #         is_active=True,
        #         status="active",
        #     )
        #     .annotate(
        #         rank=SearchRank(vector, query)
        #     )
        #     .filter(rank__gte=0.1)
        #     .order_by("-rank")
        # )
        events = (
    Event.objects.annotate(
        search=SearchVector(
            "title",
            "description",
            "venue",
            "location",
            "organization",
        )
    )
    .filter(
        search=SearchQuery(search),
        is_active=True,
        status="active",
    )
)

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                "count": events.count(),
                "results": serializer.data,
            }
        )







# showing popular events under featured section,displaying top 10 events
class ViewPopularEvents(ViewSet):

    def list(self, request):
        popular_events = (
            Event.objects
            .filter(
                is_popular=True,
                status="active"
            )
            .select_related("category")
            .order_by("-public_count")[:10]
        )

        serializer = EventSerializer(
            popular_events,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Featured events retrieved successfully.",
                "data": serializer.data
            }
        )


# class EventViewSet(ModelViewSet):
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
        
#         myProfile = MyProfile.objects.get(organizer=user)    
#             # approved!=''
#         if not myProfile.is_approved:
#             raise PermissionDenied("you are not approved to create events!")
        
#         # prevent duplicate event title
#         title = serializer.validated_data.get('title')
#         location = serializer.validated_data.get('location')
#         print(f"Creating event with title :{title} for user: {user}")

#         if Event.objects.filter(title = title , organizer=user , location=location).exists():
#             raise exceptions.ValidationError(f"{user.email} has already created this event title ")
        
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

















# view all events
# category wise ebvets
# booking system