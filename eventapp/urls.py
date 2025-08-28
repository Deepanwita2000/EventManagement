
from django.urls import path
from . import views

urlpatterns = [
   #api route
    path('add/',views.add_api_events,name='add_api_events' ),
    path('view/',views.view_api_events,name='view_api_events' ),
    # path('add/',views.add_api_events,name='add_api_events' ),
    # path('add/',views.add_api_events,name='add_api_events' ),

    #for admin panel
    
    path('admin_add_events/',views.add_events , name='admin_add_events'),
    path('admin_view_events/',views.view_events , name='admin_view_events'),
    path('admin_edit_events/<int:pk>/',views.edit_events , name='admin_edit_events'),


]
  