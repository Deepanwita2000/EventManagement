from eventapp.models import Event
from logicapp.models import Ticket
from logicapp.tasks import generate_ticket, send_booking_confirmation_email, send_payment_success_email
from .serializers import TicketSerializer
from rest_framework import status
from rest_framework.response import Response
from accountapp.authentication import JWTAuthentication
from decimal import Decimal
from accountapp.authentication import JWTAuthentication
from eventapp.models import Event
from .models import Booking
from eventapp.views import BaseClass
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
import razorpay
from django.conf import settings
from django.shortcuts import render
import razorpay
import os

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID,  RAZORPAY_KEY_SECRET )
)

class TicketViewSet(BaseClass):
    """
   {
    "name": "Early Bird",
    "event": 33,
    "price": "1000.00",
    "benefits": [
        "Middle seat",
        "provide soft drinks"
    ],
    "available_seats": 250,
    "discount": "5.00",
    "tax": "18.00"
}
    """
    queryset = Ticket.objects.filter(is_active=True)
    serializer_class = TicketSerializer
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "organizer":
            raise PermissionDenied(
                "Only organizers can create tickets."
            )

        event = serializer.validated_data["event"]
        name = serializer.validated_data["name"]

        # Ensure the organizer can create tickets only for their own event
        if event.created_by != user:
            raise PermissionDenied(
                "You can only create tickets for your own events."
            )

        # Prevent duplicate ticket names within the same event
        if Ticket.objects.filter(event=event, name=name).exists():
            raise exceptions.ValidationError(
                "This ticket already exists for the selected event."
            )

        serializer.save(created_by=user)


    def perform_update(self, serializer):
        ticket = self.get_object()
        user = self.request.user

        if user.role != "organizer":
            raise PermissionDenied(
                "Only organizers can update tickets."
            )

        if ticket.created_by != user:
            raise PermissionDenied(
                "You can update only your own tickets."
            )

        serializer.save(updated_by=user)

# for printing response
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response(
            {
                "message": "Ticket updated successfully.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )
    def perform_destroy(self, instance):
        user = self.request.user

        if user.role != "organizer":
            raise PermissionDenied(
                "Only organizers can delete tickets."
            )

        if instance.created_by != user:
            raise PermissionDenied(
                "You can delete only your own tickets."
            )

        # instance.delete()
        instance.is_active = False
        instance.updated_by=user
        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": "Ticket deleted successfully."
            },
            status=status.HTTP_200_OK
        )


class BookingViewSet(BaseClass):
    
    def create(self, request):
        user = request.user

        if user.role != "user":
            raise PermissionDenied("Only users can book tickets.")
        
        event_id = request.data.get("event_id")
        ticket_id = request.data.get("ticket_id")
        selected_seats = request.data.get("selected_seats")

        if Booking.objects.filter(event_id=event_id,ticket_id=ticket_id,created_by=user).exists():
            return Response("already booked!")

        if not event_id or not ticket_id or not selected_seats:
            raise ValidationError(
                "event_id, ticket_id and selected_seats are required."
            )

        try:
            selected_seats = int(selected_seats)
        except ValueError:
            raise ValidationError("selected_seats must be an integer.")

        if selected_seats <= 0:
            raise ValidationError(
                "selected_seats must be greater than zero."
            )

        try:
            event = Event.objects.get(id=event_id, is_active=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found.")

        try:
            ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            raise ValidationError("Ticket not found.")

        # Ensure the ticket belongs to the selected event
        if ticket.event != event:
            raise ValidationError(
                "Selected ticket does not belong to this event."
            )
        with transaction.atomic():

            if ticket.event != event:
                raise ValidationError(
                    "Selected ticket does not belong to this event."
                )

            if selected_seats > ticket.available_seats:
                raise ValidationError(
                    f"Only {ticket.available_seats} seats are available."
                )

            # Calculate amount
            base_amount = ticket.price * Decimal(selected_seats)

            discount_amount = Decimal("0")
            if ticket.discount:
                discount_amount = (
                    base_amount * ticket.discount
                ) / Decimal("100")

            subtotal = base_amount - discount_amount

            tax_amount = Decimal("0")
            if ticket.tax:
                tax_amount = (
                    subtotal * ticket.tax
                ) / Decimal("100")

            amount = subtotal + tax_amount

            ticket.available_seats -= selected_seats
            ticket.save()
            expires_at = timezone.now() + timedelta(minutes=2)  # time 2 mins
            booking = Booking.objects.create(
                event=event,
                ticket=ticket,
                selected_seats=selected_seats,
                amount=amount,
                created_by=user,
                expires_at=expires_at

            )
            send_booking_confirmation_email.delay(
                                                user.email,
                                                user.first_name,
                                                event.title,
                                                ticket.name,
                                                selected_seats,
                                                str(amount),
                                            )

            

        return Response(
            {
                "message": "Ticket booked successfully.",
                "event":booking.event.title,
                "booking_id": booking.id,
                "amount": booking.amount,
                "payment_status": booking.payment_status,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self,request):
        user=request.user
        # all tickets
        bookings = Booking.objects.filter(created_by=user)  
        print(bookings)
        if not bookings:
            return Response({"msg":"No bookings done!!"})
        data=[]
        x={}
        for b in bookings:
            x={
                "event":b.event.title,
                "ticket":b.ticket.name,
                "discount":b.ticket.discount,
                "tax":b.ticket.tax,
                "amount":b.amount,
                "payment_status":b.payment_status
            }
            data.append(x)
        return Response({
            "data":data
        })
        







class MakePayment(BaseClass):
    """
    POST /logic/payment/
        payload:{
        "booking_id": 10
        }

    response:
    {
    "booking_id": 10,
    "order_id": "order_Q1AbCdEf12345",
    "amount": 112000,
    "currency": "INR"
}
    """

    def create(self, request):
        user = request.user
        booking_id = request.data.get("booking_id")
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            created_by=user,
            payment_status="reserved"
        )
        print("=====================================")
        print(RAZORPAY_KEY_ID)
        print(RAZORPAY_KEY_SECRET)
        print("=====================================")

        order = client.order.create({
            "amount": int(booking.amount * 100),   # paise
            "currency": "INR",
            "receipt": str(booking.id)
        })

        booking.razorpay_order_id = order["id"]
        booking.save(update_fields=["razorpay_order_id"])

        return Response({
            "message": "Order created successfully.",
            "booking_id": booking.id,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        })



    @action(detail=False, methods=["post"])
    def test_success(self, request):
        """
        POST /logic/payment/test_success/
        {
        "booking_id": 10
        }

        """

        booking = get_object_or_404(
            Booking,
            id=request.data["booking_id"],
            created_by=request.user,
            payment_status="reserved"
        )

        booking.payment_status = "paid"
        booking.razorpay_payment_id = "pay_test_12345"
        booking.razorpay_signature = "signature_test"
        booking.updated_by = request.user
        booking.save()
        print("generate_ticket")
        generate_ticket.delay(booking.id)

        # send_payment_success_email.delay(
        #     booking.created_by.email,
        #     booking.created_by.first_name,
        #     booking.event.title,
        #     booking.ticket.name,
        #     booking.selected_seats,
        #     str(booking.amount),
        # )

        return Response({
            "message": "Payment Successful, ticket sent to ur email!!"
        })
























# class PaymentPage(ViewSet):

def retrieve(request, pk=None):
        print(pk)

        booking = get_object_or_404(
            Booking,
            id=pk,
            # created_by="none",
            payment_status="reserved"
        )

        order = client.order.create({

            "amount": int(booking.amount * 100),

            "currency": "INR",

            "receipt": str(booking.id)

        })

        booking.razorpay_order_id = order["id"]
        booking.save(update_fields=["razorpay_order_id"])

        return render(
            request,
            "payments.html",
            {
                "booking": booking,
                "order": order,
                "key": RAZORPAY_KEY_ID,
            },
        )


class PaymentViewSet(ViewSet):

    @action(detail=False, methods=["post"])

    def verify(self, request):

        booking = get_object_or_404(

            Booking,

            id=request.data["booking_id"],

            # created_by="none"  ,   #request.user,

            payment_status="reserved"

        )

        params = {

            "razorpay_order_id":
                request.data["razorpay_order_id"],

            "razorpay_payment_id":
                request.data["razorpay_payment_id"],

            "razorpay_signature":
                request.data["razorpay_signature"],

        }

        try:

            client.utility.verify_payment_signature(params)

        except razorpay.errors.SignatureVerificationError:

            return Response(
                {
                    "message":"Invalid Payment"
                },
                status=400
            )

        booking.payment_status="paid"

        booking.razorpay_payment_id=params["razorpay_payment_id"]

        booking.razorpay_signature=params["razorpay_signature"]

        # booking.updated_by="none"  #request.user

        booking.save()

        send_payment_success_email.delay(
            booking.created_by.email,
            booking.created_by.first_name,
            booking.event.title,
            booking.ticket.name,
            booking.selected_seats,
            str(booking.amount),
        )

        return Response(
            {
                "message":"Payment Successful"
            }
        )

