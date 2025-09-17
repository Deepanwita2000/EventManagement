# from django.db import models

# from accountapp.models import User
# from ticket_tiers.models import Tier
# from eventapp.models import Event

# # Create your models here.
# class Ticket(models.Model):
#     PAYMENT_STATUS_CHOICES = [
#         ("paid", "Paid"),
#         ("pending", "Pending"),
#         ("failed", "Failed"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
#     tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets")
#     ticketCode = models.CharField(max_length=50, unique=True)
#     qrCodeUrl = models.ImageField(upload_to="qrCode/", blank=True, null=True)
#     payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")
#     checked_in = models.BooleanField(default=False)
#     purchased_at = models.DateTimeField(auto_now_add=True)
  
#     def __str__(self):
#         return f"{self.ticketCode} - {self.user.username} - {self.event.title}"



# # 
# # 4. tickets

# # {
# #   userId: ObjectId,
# #   eventId: ObjectId,
# #   tierId: ObjectId,
# #   ticketCode: "EVT20250720-ABC123",
# #   qrCodeUrl: "/tickets/qr/ABC123.png",
# #   paymentStatus: "paid" | "pending" | "failed",
# #   checkedIn: false,
# #   purchasedAt: ISODate()
# # }
