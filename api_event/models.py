from django.db import models

# Create your models here.
# {
#   _id: ObjectId,
#   title: "Startup Summit 2025",
#   description: "A national startup networking event",
#   location: "Bangalore",
#   date: "2025-08-20",
#   time: "18:00",
#   organizer: "TechMeet Pvt Ltd",
#   banner: "startup_summit.png",
#   status: "active" | "inactive",
#   createdBy: ObjectId
# }

class Events(models.Model):
    # id automatically created by django
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.CharField(max_length=100)
    banner = models.ImageField()

    # createdBy will be created for foreign key later on

    created_at = models.DateField(auto_now_add= True) # date will be created at the time of creating data
    updated_at = models.DateField(auto_now= True) # Automatically updates the field to the current date every time the object is saved.
 
    def __str__(self):
        return self.title