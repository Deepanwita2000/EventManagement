from django.db import models
from accountapp.models import User
# Create your models here.
class MyProfile(models.Model): # organizer's profile
    #id
    gender = models.CharField(max_length=50)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)
    contact = models.CharField(max_length=10)
    address = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer= models.ForeignKey(User , on_delete=models.CASCADE , related_name='profile') # organizer

    def __str__(self):
        return f"{self.organizer.email}-{self.gender}"
    
  