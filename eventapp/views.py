
from django.db.models.query import QuerySet
from eventapp.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import filters
from accountapp.authentication import JWTAuthentication
from eventapp.models import Event, LandscapeImage, PortraitImage
from .models import  Event
# using full-text search here
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.db.models import Q
from django.core.paginator import Paginator
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
    payload:   {"event_id":11}

    GET /events/?page=1

    Example:
    /events/?page=2
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def list(self, request):

        all_events = Event.objects.all()
        page_number = request.GET.get("page", 1)
        paginator = Paginator(all_events, 5)
        page_obj = paginator.get_page(page_number)
        serializer = EventSerializer(
            page_obj.object_list,
            many=True
        )
        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "next": page_obj.has_next(),
            "previous": page_obj.has_previous(),
            "data": serializer.data
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

















