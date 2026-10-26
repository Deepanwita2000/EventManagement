from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('ticket', views.TicketViewSet , basename='ticket-logic')   # logic/ticket/
router.register('ticket-tiers', views.ShowTicket , basename='tickets-ticket-tiers')   # logic/ticket-tiers/
router.register('ticket-info', views.ShowTicketDetails , basename='tickets-ticket-info')   # logic/ticket-info/
router.register('booking', views.BookingViewSet,basename="api-booking") # /logic/booking/

urlpatterns = [
     path('',include(router.urls)) ,

     # ========== UI ========== #
     path("pay/", views.payment_page, name="payment-page"),
     path("payment/create-order/",  views.create_payment_order,  name="create-payment-order" ),
     path("payment/verify/",views.verify_payment,name="verify-payment"),
    ]

