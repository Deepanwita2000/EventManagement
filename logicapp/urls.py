from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('ticket', views.TicketViewSet , basename='ticket-logic')   # logic/ticket/
router.register('booking', views.BookingViewSet,basename="api-booking") # /logic/booking/
router.register('payment', views.MakePayment,basename="make-paymnet") # /logic/payment/

# router.register('booking', views.MakePayment,basename="make-paymnet") # /logic/payment/
# router.register("payment",  views.PaymentViewSet, basename="payment") # for ui


urlpatterns = [
     path('',include(router.urls)) ,
#      path(
#     "payment/<int:pk>/",
#     views.retrieve,
#     name="payment-page",
# )
    ]

