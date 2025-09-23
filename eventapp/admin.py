from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Event)

class EventAdmin(admin.ModelAdmin):
    list_display=[
        'title',
        'location',
        'date',
        'time',
        'organizer',
        'category'
    ]

# admin.site.register(TrackEvents)
admin.site.register(Event,EventAdmin)