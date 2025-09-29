from django.contrib import admin
from .models import Category
# Register your models here.
class CategoryDetails(admin.ModelAdmin):
    list_display=[
        'name',
        'description'
      
    ]

# admin.site.register(TrackEvents)
admin.site.register(Category,CategoryDetails)