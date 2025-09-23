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
    languages=models.JSONField(default=list)
    age = models.CharField() # who can see the event
    organization = models.CharField(max_length=100)
    landscape = models.ImageField(upload_to="banners/", blank=False, null=False)
    portrait = models.ImageField(upload_to="banners/", blank=False, null=False)
    status = models.CharField()   #   modify required ...... will hold the choices ( "active" | "inactive")
    organizer = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role':'organizer'} , related_name='event_created')
    category = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ['title' , 'organizer'] 

    def __str__(self):  
        return self.title


