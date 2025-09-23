from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventViewSet,ReadAllEvent
router = DefaultRouter()
router.register('route', EventViewSet , basename='route')
router.register('public_route', ReadAllEvent , basename='public_route')


urlpatterns = [
      path('api/', include(router.urls)),
         path('admin_add_events/',views.add_events , name='admin_add_events'),
       path('admin_view_events/',views.view_events , name='admin_view_events'),
      path('admin_edit_events/<int:pk>/',views.edit_events , name='admin_edit_events'),
     

   ]




# urlpatterns = [
#    #api route
#     # path('add/',views.add_api_event,name='add_api_event' ),
#     # path('view/',views.view_api_event,name='view_api_event' ),
#     # path('edit/<int:pk>/',views.edit_api_event,name='edit_api_event' ),
#     # path('delete/<int:pk>/',views.delete_api_event,name='delete_api_event' ),
#     path('api/', include(router.urls)),

#     #for admin panel
    
   #  path('admin_add_events/',views.add_events , name='admin_add_events'),
   #  path('admin_view_events/',views.view_events , name='admin_view_events'),
   #  path('admin_edit_events/<int:pk>/',views.edit_events , name='admin_edit_events'),
# ]
