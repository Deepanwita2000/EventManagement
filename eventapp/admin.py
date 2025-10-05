
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
        'category',
        'is_popular'
    ]

admin.site.register(Event,EventAdmin)