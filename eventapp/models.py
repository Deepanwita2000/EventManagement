from django.db import models

# Create your models here.
class Event(models.Model):
    # id: ObjectId, autocreated
    title= models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.CharField(max_length=100)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    status = models.CharField()   #   modify required ...... will hold the choices ( "active" | "inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # createdBy = #left to add for foreign key


#   description = models.TextField()
  #  image = models.ImageField(upload_to="streams/", blank=True, null=True)
#   _id: ObjectId,
#   title: "Startup Summit 2025",
#   description: "A national startup networking event",
#   location: "Bangalore",
#   date: "2025-08-20",
#   time: "18:00",
#   organizer: "TechMeet Pvt Ltd",
#   banner: "startup_summit.png",
#   status: "active" | "inactive",
#   createdBy


