# from eventapp.models import Event
# from ticket_tiers.models import Tier
# from tickets.models import Ticket
# from rest_framework import serializers

# from accountapp.models import User

# class TicketSerializer(serializers.ModelSerializer):
#       qrCodeUrl = serializers.ImageField(max_length=None , use_url=True , required=False)

#       user = serializers.StringRelatedField()  
#       user_id =  serializers.PrimaryKeyRelatedField(source='user' ,read_only=True)   
#       user_name =  serializers.CharField(write_only=True)   

#       event = serializers.StringRelatedField(read_only=True)
#       event_id = serializers.PrimaryKeyRelatedField(source='event',read_only=True)
#       event_name = serializers.CharField(write_only=True)

#       tier = serializers.StringRelatedField(read_only=True)
#       tier_id =  serializers.PrimaryKeyRelatedField(source='tiers',read_only=True)
#       tier_name = serializers.CharField(write_only=True)

#       purchased_at= serializers.DateTimeField(read_only=True)

#       class Meta:
#             model = Ticket
#             fields=['id','user','user_name','user_id','event','event_name','event_id','tier','tier_name','tier_id','ticketCode','qrCodeUrl', 'payment_status','checked_in',
#                     'purchased_at']
      
#       def create(self,validated_data):
#             user_name = validated_data.pop('user_name')
#             print(user_name)
#             event_name = validated_data.pop('event_name')
#             tier_name = validated_data.pop('tier_name')
#             split_user=user_name.split(" ")
#             print(split_user)
#             fname = split_user[0]
#             lname = split_user[1]
            

#             try:
#                   user_info = User.objects.get(first_name=fname , last_name=lname) 
#                   print(user_info.role , user_info.last_name)
            
#             except User.DoesNotExist:
#                   raise serializers.ValidationError({"User":f"{user_name} Does not exist!"})
#             try:
#                   event_info = Event.objects.get(title=event_name) 
#                   print(event_info.title , event_info.organizer)
            
#             except Event.DoesNotExist:
#                   raise serializers.ValidationError({"event":f"{event_name} Event Does not exist!"})
            
#             # tier validation
#             try:
#                   tier_info = Tier.objects.get(name =tier_name ) 
#                   print(tier_info.name , tier_info.event.title , tier_info.price)
            
#             except Tier.DoesNotExist:
#                   raise serializers.ValidationError({"Ticket_tier":f"{tier_name} Does not exist!"})
            
#             ticket = Ticket.objects.create(user=user_info , event=event_info , tier=tier_info , **validated_data)
#             print(ticket)
#             return ticket
      
#       def update(self, instance , validated_data):
#             event_name = validated_data.pop('event_name',None)
#             tier_name = validated_data.pop('tier_name',None)
#             user_name = validated_data.pop('user_name',None)
            

#             print("instance : ",instance)
#             print("validated_data : ",validated_data)
#             if event_name:
#                   try:
#                         event = Event.objects.get(title=event_name)
#                         instance.event=event
#                   except Event.DoesNotExist:
#                         return serializers.ValidationError({"event":f"{event_name} Event Does not exist!"})
#             if tier_name:
#                   try:
#                         tier_info = Tier.objects.get(name=tier_name)
#                         instance.tier = tier_info
#                   except Tier.DoesNotExist:
#                         raise serializers.ValidationError({"Ticket_tier":f"{tier_name} Does not exist!"})
            
#             if user_name:
#                   split_name = user_name.split(" ")
#                   fname = split_name[0]
#                   lname = split_name[1]
#                   try:
#                         user_info = User.objects.get(first_name=fname , last_name=lname) 
#                         instance.user_name = user_info
            
#                   except User.DoesNotExist:
#                         raise serializers.ValidationError({"User":f"{user_name} Does not exist!"})
#             # updae other fields
#             for attr , value in validated_data.items():
#                   setattr(instance , attr , value)
            
#             instance.save()
#             return instance
                        

          


