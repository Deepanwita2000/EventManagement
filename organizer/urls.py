from django.urls import include, path
from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('route', ProfileViewSet , basename='route')



urlpatterns = [
      path('api/', include(router.urls)),
      

   ]

