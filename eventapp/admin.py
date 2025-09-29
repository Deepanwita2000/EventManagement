
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

# admin.site.register(TrackEvents)
# =======
# from django.contrib import admin
# from .models import *
# # Register your models here.
# # admin.site.register(Event)

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
# >>>>>>> 3c71da83ca8249c58b92e6741917a4e4aada0e7c
# admin.site.register(Event,EventAdmin)