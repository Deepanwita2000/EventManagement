# from django.contrib import admin
# from django.urls import path,include
# from . import views,settings
# from django.conf.urls.static import static
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )

# from rest_framework.permissions import AllowAny

# urlpatterns = [
    
#     path('admin/', admin.site.urls),
#     # path('' , views.home , name='home'),
#     path('event/', include('eventapp.urls')),  
#     path('account/', include('accountapp.urls')),
#     path('logic/', include('logicapp.urls')),


#     # OpenAPI schema
#     path("api/schema/",SpectacularAPIView.as_view( permission_classes=[AllowAny]),name="schema"),
#     # Swagger UI
#     path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny]),name="swagger-ui"),
#     # ReDoc
#     path("api/redoc/",SpectacularRedocView.as_view(url_name="schema", permission_classes=[AllowAny] ), name="redoc"),
# ]
  
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.conf.urls.static import static

from rest_framework.permissions import AllowAny

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [

    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),
    path('event/', include('eventapp.urls')),
    path('account/', include('accountapp.urls')),
    path('logic/', include('logicapp.urls')),

    # OpenAPI Schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(
            permission_classes=[AllowAny]
        ),
        name="schema"
    ),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            permission_classes=[AllowAny]
        ),
        name="swagger-ui"
    ),

    # ReDoc
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
            permission_classes=[AllowAny]
        ),
        name="redoc"
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

