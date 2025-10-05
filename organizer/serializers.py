from rest_framework import serializers
from .models import MyProfile
from datetime import date,datetime
class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True , required=False)
    # stream_name = serializers.CharField(write_only=True)  # Accept from Stream name as input inside POST
    organizer = serializers.StringRelatedField(read_only=True)  # Display stream name in response
    # stream_id = serializers.PrimaryKeyRelatedField(source='stream', read_only=True)

    class Meta:
        model = MyProfile
        fields = [
                  'id',
                 'gender',
                'image' ,
                'contact',
                'address',
                'organizer',
                'is_approved'
                ]
        
    