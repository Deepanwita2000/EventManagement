# from django.db import models

# # Create your models here.
# class Event(models.Model):
#     # id: ObjectId, autocreated
#     title= models.CharField(max_length=100)
#     description = models.TextField()
#     location = models.CharField(max_length=100)
#     venue = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     language = models.CharField(max_length=100) #added 
#     age = models.CharField() #added
#     organizer = models.CharField(max_length=100)
#     banner = models.ImageField(upload_to="banners/", blank=True, null=True)
#     status = models.CharField()   #   modify required ...... will hold the choices ( "active" | "inactive")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # createdBy = #left to add for foreign key

#     def __str__(self):  
#         return self.title




from django.db import models
from accountapp.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Event(models.Model):

    # id: ObjectId, autocreated
    title= models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    venue = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField()
    language = ArrayField(
        models.CharField(max_length=30),
        blank=True,
        default=list
    )
    # duration = start_time-end_time # calculate the duration
    age = models.CharField() # who can see the event
    organization = models.CharField(max_length=100)

    # store image paths as dictionary
    # images = models.JSONField(upload_to="banners/" , default=dict, blank=True, null=True)

    wallpaper = models.ImageField(upload_to="banners/", blank=False, null=False)
    portrait = models.ImageField(upload_to="banners/", blank=False, null=False)
    status = models.CharField()   #   modify required ...... will hold the choices ( "active" | "inactive")
      
    organizer = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role':'organizer'} , related_name='event_created')
    
    is_approved = models.BooleanField(default=False) # get approval from admin
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ['title' , 'organizer'] 

    def __str__(self):  
        return self.title


