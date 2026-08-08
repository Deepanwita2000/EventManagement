from django.db import models

# Create your models here.
from django.db import models
from eventapp.models import Event
from accountapp.models import BaseModel, User



class Ticket(BaseModel):
    name = models.CharField(max_length=100)

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    benefits = models.JSONField(default=list)

    available_seats = models.PositiveIntegerField(default=0)

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    tax = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=12
    )
    # is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.name





from django.db import models
from accountapp.models import User,BaseModel
from eventapp.models import Event
# from ticket_tiers.models import Tier
# from ticketapp.models import Ticket



class Booking(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("expired", "Expired"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    selected_seats = models.PositiveIntegerField(default=1)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="reserved",
    )

    expires_at = models.DateTimeField(null=True , blank=True)
    razorpay_order_id = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    razorpay_payment_id = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    razorpay_signature = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.created_by} - {self.event}"




from django.db import models
from logicapp.models import Booking

class EventTicket(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="issued_ticket"
    )

    ticket_number = models.CharField(
        max_length=30,
        unique=True
    )

    pdf = models.FileField(
        upload_to="tickets/pdf/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_number
# class EventTicket(models.Model):
#     booking = models.OneToOneField(
#         Booking,
#         on_delete=models.CASCADE,
#         related_name="event_ticket"
#     )

#     ticket_number = models.CharField(
#         max_length=30,
#         unique=True
#     )

#     qr_code = models.ImageField(
#         upload_to="tickets/qr/",
#         null=True,
#         blank=True
#     )

#     pdf = models.FileField(
#         upload_to="tickets/pdf/",
#         null=True,
#         blank=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.ticket_number