from django.db import models
from eventapp.models import Event
# Create your models here.
class Tier(models.Model):
    event = models.ForeignKey(Event , on_delete=models.CASCADE , related_name="tier") # will hold the primary key of Event table
    name = models.CharField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    quantityAvailable = models.IntegerField()
    benefits = models.JSONField() # ["Front row", "Free swag"]


    def __str__(self):
        return f"{self.event.title}-{self.price}"


# {
#   _id: ObjectId,
#   eventId: ObjectId,
#   name: "VIP",
#   price: 2000,
#   quantityAvailable: 100,
#   benefits: ["Front row", "Free swag"]
# }

