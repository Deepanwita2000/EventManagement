from django.shortcuts import render
from api_event.models import Events
from django.db.models.query import QuerySet
from api_event.serializers import EventSerialiser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 


# Create your views here.
@api_view(['GET'])
def view_events(request):
    events :QuerySet = Events.objects.all()
    all_events :list[dict]= EventSerialiser(events, many=True).data #coverting queryset into python native data

    if not all_events:
        return Response({"message": "No events found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message" : "List of all events", "events": all_events}, status=status.HTTP_200_OK)





