
from django.urls import path
from . import views

urlpatterns = [
   #api route
    path('add_tier/',views.api_add_tier,name='api_add_tier' ),
    path('view_tier/',views.api_view_tier,name='api_view_tier' ),
    path('edit_tier/<int:pk>/',views.api_edit_tier,name='api_edit_tier' ),
    path('del_tier/<int:pk>/',views.api_delete_tier,name='api_delete_tier' ),

    #for admin panel
    
   



]
  