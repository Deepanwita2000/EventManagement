from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError

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
    image = models.ImageField(upload_to="banners/", blank=False, null=False)
    is_approved=models.BooleanField(default=False)  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def clean(self):
        # Mandatory image for organizers
        if self.role == self.ORGANIZER and not self.image:
            raise ValidationError("Organizer must have an image.")

    def __str__(self):
        return self.email 


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} (Expires: {self.expired_at})"
    
