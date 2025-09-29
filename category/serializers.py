from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None , use_url=True , required=False)
    class Meta:
        model = Category
        fields = ['id', 'name','image', 'description']