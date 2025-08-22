from rest_framework import serializers
from api_event.models import Events

class EventSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id','title','location','date','time','organizer','banner']

        def validate_title(self,value):
             if str(value).isdigit():
                    raise serializers.ValidationError("title must not be a number.")
             
             if Events.objects.filter(title__iexact=value).exists():
                    raise serializers.ValidationError("Stream with this name already exists.")
             return value
        

        def validate_location(self,value):
                if str(value).isdigit():
                    raise serializers.ValidationError("title must not be a number.")
             
                if Events.objects.filter(location__iexact=value).exists():
                    raise serializers.ValidationError("Stream with this name already exists.")
                
                return value
        
        
        def validate_date(self,value):
             pass
        
        def validate_time(self,value):
             pass

        def validate_organizer(self,value):
             if str(value).isdigit():
                    raise serializers.ValidationError("title must not be a number.")
        
        def validate_banner(self,value):
             pass





#     from rest_framework import serializers
# from streamapp.models import Stream

# class StreamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stream
#         fields = ['id', 'name', 'description']

#     def validate_name(self, value):
#         # Check if name is only digits
#         if str(value).isdigit():
#             raise serializers.ValidationError("Name must not be a number.")

#         # Check if name already exists (case-insensitive)
#         if Stream.objects.filter(name__iexact=value).exists():
#             raise serializers.ValidationError("Stream with this name already exists.")

#         return value

#     def validate_description(self, value):
#         if not value.strip():
#             raise serializers.ValidationError("Description cannot be blank.")
#         return value