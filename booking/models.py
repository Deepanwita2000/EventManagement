from django.db import models
from accountapp.models import User
from eventapp.models import Event
from ticket_tiers.models import Tier

# Create your models here.
class Booking(models.Model):
    ROLE_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("failed", "Failed"),
    ]

    #id autocreated
    user = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'role':'user'} , related_name='bookings')
    event = models.ForeignKey(Event , on_delete=models.CASCADE , related_name='bookings')
    ticket_tier = models.ForeignKey(Tier , on_delete=models.CASCADE , related_name='bookings')
    select_seats=models.IntegerField()
    booked_on =  models.DateTimeField(auto_now_add=True)
    discount =  models.DecimalField(max_digits=5 , decimal_places=2 ,null=True , blank=True)
    tax =  models.DecimalField(max_digits=5 , decimal_places=2 ,null=True , blank=True)
    total=models.DecimalField(max_digits=10 , decimal_places=2)
    paymentStatus=models.CharField(
        
        choices=ROLE_CHOICES,
        default="pending"
    )
    

    # class Meta:
        # unique_together = ['event', 'ticket_tier']  # No duplicate enrollments

    def __str__(self):
        return f"{self.user} - {self.event} -{self.ticket_tier} "
