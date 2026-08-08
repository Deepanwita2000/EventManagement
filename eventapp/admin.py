
from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Event)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=[
        "id",
        'title',
        'location',
        'date',
        'time',
        'created_by__first_name',
        'category__name',
        'is_popular'
    ]

# admin.site.register(Event,EventAdmin)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["id","name"]