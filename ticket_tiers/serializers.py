from rest_framework import serializers

from eventapp.models import Event
from .models import Tier

class TierSerializers(serializers.ModelSerializer):
    event = serializers.StringRelatedField(read_only=True)  # Display event name in response
    event_title = serializers.CharField(write_only=True)  # Accept from event name as input inside POST
    event_id =  serializers.PrimaryKeyRelatedField(source='event', read_only=True)

    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model= Tier
        fields=['id','ticket_types','seats','event','event_title','event_id','organizer']

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
    

    






    #         event = models.ForeignKey(Event , on_delete=models.CASCADE , related_name="tiers") # will hold the primary key of Event table
    # name = models.CharField()
    # price = models.DecimalField(max_digits=8 , decimal_places=2)
    # quantityAvailable = models.IntegerField()
    # benefits = models.JSONField() # ["Front row", "Free swag"]
    #     stream_name = serializers.CharField(write_only=True)  # Accept from Stream name as input inside POST
    # stream = serializers.StringRelatedField(read_only=True)  # Display stream name in response
    # stream_id = serializers.PrimaryKeyRelatedField(source='stream', read_only=True)

#    ticket_types = models.JSONField(default=dict)
#     seats = models.JSONField(default=dict)
#     event = models.ForeignKey(Event , on_delete=models.CASCADE , related_name="tier") # will hold the primary key of Event table
#     organizer = models.ForeignKey(User , on_delete=models.CASCADE ,limit_choices_to={'role': 'organizer'},  related_name="tier")
