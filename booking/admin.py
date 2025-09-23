from django.contrib import admin
from .models import Booking
# Register your models here.

class BookingDetails(admin.ModelAdmin):
    list_display=[
        'user',
        'event',
        'ticket_tier', 
        'booked_on',
        'paymentStatus'
    ]
admin.site.register(Booking,BookingDetails)

# class EventAdmin(admin.ModelAdmin):
#     list_display=[
#         'title',
#         'location',
#         'date',
#         'time',
#         'organizer',
#         'category'
#     ]

# # admin.site.register(TrackEvents)
# admin.site.register(Event,EventAdmin)