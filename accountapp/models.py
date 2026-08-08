from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.conf import settings
class User(AbstractUser):
    ADMIN = 'admin'
    ORGANIZER = 'organizer'
    USER = 'user'
  
    # Role choices
    ROLE_CHOICES = [
         (ADMIN, 'Admin'),
         (ORGANIZER, 'Organizer'),
        (USER, 'User')
     ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # image = models.ImageField(upload_to="profile/", blank=False, null=False)
    is_approved=models.BooleanField(default=False)  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # def clean(self):
    #     # Mandatory image for organizers
    #     if self.role == self.ORGANIZER and not self.image:
    #         raise ValidationError("Organizer must have an image.")

    def __str__(self):
        return self.email 


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} (Expires: {self.expired_at})"
    

class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="%(class)s_updated",null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class MyProfile(BaseModel): # organizer's profile
    #id
    gender = models.CharField(max_length=50)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)
    contact = models.CharField(max_length=10)
    address = models.TextField()
    is_approved = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # organizer= models.ForeignKey(User , on_delete=models.CASCADE , related_name='profile') # organizer

    def __str__(self):
        return f"{self.created_by.email}-{self.gender}"
    
  