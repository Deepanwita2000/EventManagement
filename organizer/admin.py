from django.contrib import admin

# Register your models here.
from .models import MyProfile
# Register your models here.
# admin.site.register(Event)

class OrganizerProfile(admin.ModelAdmin):
    list_display=[
       'gender',
'image',
'contact',

'organizer'
   
    ]

admin.site.register(MyProfile,OrganizerProfile)