
from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display =  [
        'id',
                        'first_name', 
                        'last_name',
                        'role',
                        'email',
                        'is_approved'
                    ]

admin.site.register(User,UserAdmin)



@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display=[
        'id','user','token'
    ]

@admin.register(MyProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=[
        "id","gender","is_approved"
    ]



