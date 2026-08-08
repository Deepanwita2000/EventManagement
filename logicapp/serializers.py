from rest_framework import serializers
from eventapp.models import Event
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
   
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    event_title = serializers.CharField(source="event.title", read_only=True)

    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "name",
            "event",
            "event_id",
            "event_title",
            "price",
            "benefits",
            "available_seats",
            "discount",
            "tax",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate_price(self, value):
        if value > 5000:
            raise serializers.ValidationError(
                "Price cannot be greater than 5000."
            )
        return value



