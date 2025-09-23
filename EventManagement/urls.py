
from django.contrib import admin
from django.urls import path,include
from . import views,settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.home , name='home'),
    path('event/', include('eventapp.urls')),
    path('tiers/', include('ticket_tiers.urls')),
    path('account/', include('accountapp.urls')),
    path('booking/', include('booking.urls')),
]
  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)