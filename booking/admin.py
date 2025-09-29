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
# =======
# from django.contrib import admin
# from .models import Booking
# # Register your models here.

# class BookingDetails(admin.ModelAdmin):
#     list_display=[
#         'user',
#         'event',
#         'ticket_tier', 
#         'booked_on',
#         'paymentStatus'
#     ]
# admin.site.register(Booking,BookingDetails)

# # class EventAdmin(admin.ModelAdmin):
# #     list_display=[
# #         'title',
# #         'location',
# #         'date',
# #         'time',
# #         'organizer',
# #         'category'
# #     ]

# # # admin.site.register(TrackEvents)
# >>>>>>> 3c71da83ca8249c58b92e6741917a4e4aada0e7c
# # admin.site.register(Event,EventAdmin)