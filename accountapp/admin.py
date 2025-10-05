
from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display =  [
                        'first_name', 
                        'last_name',
                        'role',
                        'email',
                        'is_approved'
                    ]

admin.site.register(User,UserAdmin)


# =======
# from django.contrib import admin
# from .models import *
# # Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     list_display =  [
#                         'first_name', 
#                         'last_name',
#                         'role',
#                         'email',
#                         'is_approved'
#                     ]

# admin.site.register(User,UserAdmin)


# >>>>>>> 3c71da83ca8249c58b92e6741917a4e4aada0e7c
# admin.site.register(UserToken)