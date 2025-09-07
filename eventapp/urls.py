
from django.urls import path
from . import views

urlpatterns = [
   #api route
    path('add/',views.add_api_event,name='add_api_event' ),
    path('view/',views.view_api_event,name='view_api_event' ),
    path('edit/<int:pk>/',views.edit_api_event,name='edit_api_event' ),
    path('delete/<int:pk>/',views.delete_api_event,name='delete_api_event' ),

    #for admin panel
    
    path('admin_add_events/',views.add_events , name='admin_add_events'),
    path('admin_view_events/',views.view_events , name='admin_view_events'),
    path('admin_edit_events/<int:pk>/',views.edit_events , name='admin_edit_events'),


]
  