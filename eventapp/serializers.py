from rest_framework import serializers
from eventapp.models import Event
from datetime import date,datetime
class EventSerializer(serializers.ModelSerializer):
    landscape = serializers.ImageField(max_length=None , use_url=True , required=False)
    portrait = serializers.ImageField(max_length=None , use_url=True , required=False)
    # available_seats = serializers.IntegerField(read_only=True)
    # images = serializers.JSONField(default=dict , read_only=True)
    #images :{"wallpaper":wallpaper,"portrait":portrait}

    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = [
                    'id',
                  'title',
                  'description',
                  'category',
                  'organization',
                  'location',
                  'languages',
                  'age','venue','date','time',
                  'duration','organizer',
                  'landscape','portrait',
                  'age','organizer',
                  'status',
                  ]
    
        
    def validate_title(self,value):
        if str(value).isdigit():
            raise serializers.ValidationError("Name must not be a number")
        return value
    
    # def validate_description(self , value):
    #     if len(str(value)) > 100:
    #          raise serializers.ValidationError("description must be within 150 characters long.")
    #     return value
    
    # def validate_available_seats(self, value):
    #     if value == 0:
    #         raise serializers.ValidationError("No seats available..")
        


    def validate_location(self,value):
        return value
    
    def validate_venue(self,value):
        if len(str(value)) > 100:
             raise serializers.ValidationError("description must be within 150 characters long.")
        return value
    
    def validate_date(self,value):
        date_string=str(value)
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        if date_object < date.today():
            raise serializers.ValidationError("Invalid date")
        
        # later on for formated date

        return value
    
    def validate_language(self,value):

        split_value = value[0].split(",")
        print(type(split_value))
        return split_value

    
    #current_date = date.today()
    def validate_time(self,value):
        return value

    def validate_organization(self,value):
        if len(str(value)) > 80:
             raise serializers.ValidationError("description must be within 80 characters long.")
        return value
    

    
    def validate_status(self,value):
        if str(value) not in ("active" , "inactive"):
            raise serializers.ValidationError("Invalid status")
        return value
    
    # def create(self,validated_data):
    #     seats = validated_data.get('seats')
    #     print(seats)
    #     sum = 0
    #     for k , v in seats.items():
    #         sum = sum+v
    #     available_seats = sum
    #     event = Event.objects.create(available_seats=available_seats, **validated_data)
    #     return event
    #     pass

    # def update():
    #     pass

    # def create(self, validated_data):
    #     print(validated_data)
    #     stream_name = validated_data.pop('stream_name') # Extracting the stream_name from JSON and removing it as well
    #     print(stream_name)
    #     print(validated_data)
    #     try:
    #         # So whatever stream_name I gave in POST based on that it will search the Stream ID
    #         stream = Stream.objects.get(name=stream_name)   
    #         print((stream.name , stream.description))  
    #     except Stream.DoesNotExist:
    #         raise serializers.ValidationError({'stream_name': 'Stream not found.'})
        
    #     subject = Subject.objects.create(stream=stream, **validated_data)
    #     print(subject)
    #     return subject