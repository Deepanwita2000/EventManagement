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

@api_view(['POST'])
def add_api_event(request):
    serializer = EventSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()

        events = Event.objects.all()
        all_events=EventSerializer(events , many=True).data
        return Response({
            'message':'events registrered successfully!!',
            'events': all_events,
        },status=status.HTTP_201_CREATED)
    
    else:
        return Response({
            'message':'events registrered failed!!',
            'error': serializer.errors,
        },status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_api_event(request):
    events = Event.objects.all()
    all_events=EventSerializer(events , many=True).data
    if all_events:
        return Response({
            'message':'events registrered successfully!!',
            'events': all_events,
        },status=status.HTTP_200_OK)

    else:
        return Response({
            'message':'events registrered failed!!',
                 },status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT', 'PATCH'])
def edit_api_event(request,pk):
     try:
          event = Event.objects.get(id=pk)
     except Event.DoesNotExist:
          raise Response({"error":"Event not found."},status=status.HTTP_404_NOT_FOUND)
     serializer = EventSerializer(instance=event , data=request.data , partial=(request.method == 'PATCH'))

     if serializer.is_valid():
          serializer.save()
          return Response(serializer.data , status=status.HTTP_200_OK)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_api_event(request,pk):
    try :
          event_info = Event.objects.get(id=pk)
          event_info.delete()
          return Response({"message": "Event deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Event.DoesNotExist:
         return Response({"message": "Event not found."}, status=status.HTTP_404_NOT_FOUND) 



