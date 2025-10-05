from rest_framework import serializers
from eventapp.models import Event
from category.models import Category
from datetime import date,datetime
class EventSerializer(serializers.ModelSerializer):
    landscape = serializers.ImageField(max_length=None , use_url=True , required=False)
    portrait = serializers.ImageField(max_length=None , use_url=True , required=False)
    status = serializers.CharField(read_only=True)
    # is_popular = serializers.BooleanField(read_only=True)

    organizer = serializers.StringRelatedField(read_only=True)

    category = serializers.StringRelatedField(read_only=True)  # Display stream name in response
    category_name = serializers.CharField(write_only=True)  # Accept from Stream name as input inside POST
    # category_id = serializers.PrimaryKeyRelatedField(source='category', read_only=True)

    # stream_name = serializers.CharField(write_only=True)  # Accept from Stream name as input inside POST
    # stream = serializers.StringRelatedField(read_only=True)  # Display stream name in response
    # stream_id = serializers.PrimaryKeyRelatedField(source='stream', read_only=True)

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
                  'is_popular',
                  'category',
                  'category_name'
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

    def create(self, validated_data):
        print(validated_data)
        category_name = validated_data.pop('category_name') # Extracting the category_name from JSON and removing it as well
        print(category_name)
        print(validated_data)
        try:
            # So whatever stream_name I gave in POST based on that it will search the Stream ID
            category = Category.objects.get(name=category_name)   
            print((category.name , category.description))  
        except Category.DoesNotExist:
            raise serializers.ValidationError({'Category': 'Category not found.'})
        
        event = Event.objects.create(category=category, **validated_data)
        
        return event

