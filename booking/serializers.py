import re
from rest_framework import serializers
from .models import Booking
from accountapp.models import User
from eventapp.models import Event
from ticket_tiers.models import Tier




class BookSerializer(serializers.ModelSerializer):
    event =serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(write_only=True)
    event_id = serializers.PrimaryKeyRelatedField(source='event', read_only=True)

    ticket_tier = serializers.StringRelatedField(read_only=True)
    ticket_tier_name = serializers.CharField(write_only=True)
    ticket_tier_id = serializers.PrimaryKeyRelatedField(source='ticket_tier', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    total = serializers.DecimalField(max_digits=10 , decimal_places=2,read_only=True)

    class Meta:
        model = Booking
        fields=['id' , 'event' , 'event_title','event_id','ticket_tier','ticket_tier_name','ticket_tier_id','select_seats' ,'total','booked_on', 'paymentStatus','user']

    # def validate_seats(self,value):
    #     ticket_tier_name = validated_data.pop('ticket_tier_name') 
    #     seats_info = Tier.objects.get(name = )

   
    def create(self, validated_data):
        # print(validated_data)
        request = self.context.get("request")
        user = request.user
        event_title = validated_data.pop('event_title')
        ticket_tier_name = validated_data.pop('ticket_tier_name') 
        print(ticket_tier_name)

        #fetching seat numbers
        select_seats = validated_data.get('select_seats') 
       
        tier_info = Tier.objects.get(name = ticket_tier_name)
        if select_seats <= tier_info.available_seats:
            tier_info.available_seats=tier_info.available_seats - select_seats
            print(tier_info.available_seats)
            tier_info.save()
        else:
            raise serializers.ValidationError({'seats': 'invalid seats number.'})

        p = tier_info.price
        price = p*select_seats
        tax = tier_info.tax
        discount = tier_info.discount
        # calculate price
        if tax:
            price = price + (tax/100)*price
        if discount:
            price = price - (discount/100)*price
        # tier_info.save()



        try:
            # So whatever stream_name I gave in POST based on that it will search the Stream ID
            event = Event.objects.get(title=event_title)   
            ticket = Tier.objects.get(name=ticket_tier_name)   
            print((ticket.name))  
        except Event.DoesNotExist:
            raise serializers.ValidationError({'event_title': 'Event not found.'})
        
        except Tier.DoesNotExist:
            raise serializers.ValidationError({'ticket': 'Ticket name not found.'})
        
        booking = Booking.objects.create(ticket_tier=ticket, event=event,total=price,tax=tax ,discount=discount,user=user ,**validated_data)
        
        return booking
    

#  booked_on =  models.DateTimeField(auto_now_add=True)
#     discount =  models.DecimalField(max_digits=5 , decimal_places=2 ,null=True , blank=True)
#     tax =  models.DecimalField(max_digits=5 , decimal_places=2 ,null=True , blank=True)
#     total=models.DecimalField(max_digits=10 , decimal_places=2)


    # def update(self, instance, validated_data):
    #     stream_name = validated_data.pop('stream_name', None)  # Optional during PATCH
    #     if stream_name:
    #         try:
    #             stream = Stream.objects.get(name=stream_name)
    #             instance.stream = stream
    #         except Stream.DoesNotExist:
    #             raise serializers.ValidationError({'stream_name': 'Stream not found.'})
        
    #     # Update other fields like name
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     instance.save()
    #     return instance
    
    

# # 3. Enrollment Serializer
# class EnrollmentSerializer(serializers.ModelSerializer):
#     student = serializers.StringRelatedField(read_only=True)
#     course = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Enrollment
#         fields = ['id', 'student', 'course', 'enrolled_on']


#   stream_name = serializers.CharField(write_only=True)  # Accept from Stream name as input inside POST
#     stream = serializers.StringRelatedField(read_only=True)  # Display stream name in response
#     stream_id = serializers.PrimaryKeyRelatedField(source='stream', read_only=True)