from django.db import models
from accountapp.models import User
# from category.models import Category
from django.conf import settings
from django.db import models




# class Event(models.Model):
#     # id: ObjectId, autocreated
#     title= models.CharField(max_length=100)
#     description = models.TextField()
#     location = models.CharField(max_length=100)
#     venue = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     duration = models.CharField()
#     languages=models.JSONField(default=list)
#     age = models.CharField() # who can see the event
#     organization = models.CharField(max_length=100)
#     landscape = models.ImageField(upload_to="banners/", blank=False, null=False)
#     portrait = models.ImageField(upload_to="banners/", blank=False, null=False)
#     organizer = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role':'organizer'} , related_name='event_created')
    
    
#     # admin
#     is_popular = models.BooleanField(default=False) # admin will set value
#     status = models.CharField(default="active")   #   set by admin later will hold the choices ( "active" | "inactive")
#     category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='category')
   
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 

#     class Meta:
#         unique_together = ['title' , 'organizer'] 

#     def __str__(self):  
#         return self.title





class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_updated",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(models.Model):
    #id
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="category/", blank=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=225)
    venue = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    languages = models.JSONField(default=list)
    age = models.CharField(max_length=30)
    organization = models.CharField(max_length=225)
    is_popular = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default="active")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="events")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "created_by"],name="unique_event_title_per_creator")
        ]

    def __str__(self):
        return self.title


class LandscapeImage(BaseModel):
    image = models.ImageField(upload_to="landscape/")
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name="landscapes")


class PortraitImage(BaseModel):
    image = models.ImageField(upload_to="portrait/")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="portraits")


