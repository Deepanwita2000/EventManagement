from rest_framework import serializers
from eventapp.models import Event
from datetime import date,datetime
class EventSerializer(serializers.ModelSerializer):
    wallpaper = serializers.ImageField(max_length=None , use_url=True , required=False)
    portrait = serializers.ImageField(max_length=None , use_url=True , required=False)
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = [
                    'id',
                  'title',
                  'description',
                  'organization',
                  'location',
                  'language',
                  'age','venue','date','time',
                  'duration','organizer',
                  'wallpaper','portrait',
                  'age','organizer',
                  'status',
                  'is_approved'
                  ]
        
    def validate_title(self,value):
        if str(value).isdigit():
            raise serializers.ValidationError("Name must not be a number")
        return value
    
    def validate_description(self , value):
        if len(str(value)) > 100:
             raise serializers.ValidationError("description must be within 150 characters long.")
        return value
    
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
    
    # def create():
    #     pass

    # def update():
    #     pass

