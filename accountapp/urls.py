
from django.urls import include, path
from .views import   RegisterAPIView,LoginAPIView,UserAPIView,LogoutAPIView
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('events', EventViewSet)

urlpatterns = [
    path('register/', RegisterAPIView.as_view() , name='register'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('user/', UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
    # path('api/', include(router.urls)),

# =======
# from django.urls import include, path
# from .views import   RegisterAPIView,LoginAPIView,UserAPIView,LogoutAPIView
# # from rest_framework.routers import DefaultRouter


# # router = DefaultRouter()
# # router.register('events', EventViewSet)

# urlpatterns = [
#     path('register/', RegisterAPIView.as_view() , name='register'),
#     path('login/', LoginAPIView.as_view(),name='login'),
#     path('user/', UserAPIView.as_view()),
#     path('logout/', LogoutAPIView.as_view()),

#     # path('api/', include(router.urls)),

# >>>>>>> 3c71da83ca8249c58b92e6741917a4e4aada0e7c
# ]