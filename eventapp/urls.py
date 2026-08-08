from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CreateEventViewSet,AllEvents,FilterEvents,CustomSearch

router = SimpleRouter()
router.register("api", CreateEventViewSet, basename="events") # event/api/
router.register("all-events", AllEvents, basename="all-events") # event/all-events/
router.register("filter-events", FilterEvents, basename="filter-events") # event/filter-events/
router.register("custom-search", CustomSearch, basename="custom-search") # event/custom-search/

urlpatterns = [
    path("", include(router.urls)),  # event/
]

