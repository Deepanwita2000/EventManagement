from rest_framework import serializers
from eventapp.models import Event, PortraitImage,LandscapeImage,Category
# from category.models import Category
from datetime import date,datetime

class LandscapeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = LandscapeImage
        fields = ['id', 'image']
    def get_image(self, obj):
            request = self.context.get("request")

            if obj.image:
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url

            return None


class PortraitSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = PortraitImage
        fields = ['id', 'image']
    def get_image(self, obj):
                request = self.context.get("request")
    
                if obj.image:
                    if request:
                        return request.build_absolute_uri(obj.image.url)
                    return obj.image.url
    
                return None











from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    landscapes = LandscapeSerializer(many=True, read_only=True)
    portraits = PortraitSerializer(many=True, read_only=True)

    # Accept category ID in request
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    # Show category name in response
    category_name = serializers.SerializerMethodField()

    # created_by = serializers.StringRelatedField(read_only=True)
    # updated_by = serializers.StringRelatedField(read_only=True)
    # status = serializers.CharField(read_only=True)

    class Meta:
        model = Event
        
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_name",
            "organization",
            "location",
            "languages",
            "age",
            "venue",
            "date",
            "time",
            "duration",
            "portraits",
            "landscapes",
            # "status",
            # "is_popular",
            # "created_by",
            # "updated_by",
        ]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def validate_title(self, value):
        if str(value).isdigit():
            raise serializers.ValidationError(
                "Name must not be a number."
            )
        return value

    def validate_location(self, value):
        return value

    def validate_venue(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Venue must be within 100 characters."
            )
        return value

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Invalid date.")
        return value

    # NOTE: Field name must match the model field name
    def validate_languages(self, value):
        # Handles form-data like ["English,Hindi"]
        if (
            isinstance(value, list)
            and len(value) == 1
            and isinstance(value[0], str)
            and "," in value[0]
        ):
            return [lang.strip() for lang in value[0].split(",")]

        return value

    def validate_time(self, value):
        return value

    def validate_organization(self, value):
        if len(value) > 80:
            raise serializers.ValidationError(
                "Organization must be within 80 characters."
            )
        return value

    def create(self, validated_data):
        

        event = Event.objects.create(**validated_data)

        

        return event












