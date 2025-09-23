from rest_framework import serializers

from eventapp.models import Event
from .models import Tier

class TierSerializers(serializers.ModelSerializer):
    event = serializers.StringRelatedField(read_only=True)  # Display event name in response
    event_title = serializers.CharField(write_only=True)  # Accept from event name as input inside POST
    # event_id =  serializers.PrimaryKeyRelatedField(source='event', read_only=True)

    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model= Tier
        fields=['id','name','event','event_title','benefits','available_seats','discount','tax','organizer','price']

    def create(self,validated_data):
        event_title = validated_data.pop('event_title')  
        try:
            event = Event.objects.get(title=event_title)
            # print(event.id, event.title , event.location)
        except Event.DoesNotExist:
            raise serializers.ValidationError({"event_title":"Event not found!!"})
        # Model:Tiers
        tier = Tier.objects.create(event=event , **validated_data)
        print(tier)
        return tier


    def update(self, instance , validated_data):
        print(instance)
        print(validated_data)
        event_title = validated_data.pop('event_title', None)  # Optional during PATCH
        if event_title:
            try:
                event = Event.objects.get(title=event_title)
                print(instance , event)
                instance.event = event
            except Event.DoesNotExist:
                raise serializers.ValidationError({"event_title":"Event not found!!"})
        
        # Update other fields like name
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

  