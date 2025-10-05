from django.contrib import admin
from .models import Tier
# Register your models here.
class TicketDetails(admin.ModelAdmin):
    list_display=[
        'name',
        'event',
        'organizer',
        'price',
        'available_seats'  
    ]

admin.site.register(Tier,TicketDetails)