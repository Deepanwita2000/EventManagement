from django.urls import path,include
from . import views
from .views import TierViewSet, ReadAllTickets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('route', TierViewSet , basename='route')
router.register('public_route', ReadAllTickets , basename='public_route')


urlpatterns = [
   #api route
    # path('add_tier/',views.api_add_tier,name='api_add_tier' ),
    # path('view_tier/',views.api_view_tier,name='api_view_tier' ),
    # path('edit_tier/<int:pk>/',views.api_edit_tier,name='api_edit_tier' ),
    # path('del_tier/<int:pk>/',views.api_delete_tier,name='api_delete_tier' ),
    path('api_tiers/',include(router.urls))

    #for admin panel
    # 
   



]

