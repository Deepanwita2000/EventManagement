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
from django.shortcuts import get_object_or_404
import razorpay,os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_not_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Booking
from .tasks import generate_ticket
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID,  RAZORPAY_KEY_SECRET ))


#show all tckets

class ShowTicket(ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        event_id = request.data.get("event_id")

        if not event_id:
            return Response(
                {"msg": "event_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tickets = Ticket.objects.filter(event_id=event_id)

        serializer = TicketSerializer(tickets, many=True)

        fields = [
            {
                "name": ticket["name"],
                "event": ticket["event"],
                "event_id": ticket["event"],
                "event_title": ticket["event_title"],
                "price": ticket["price"],
                "benefits": ticket["benefits"],
                "available_seats": ticket["available_seats"],
            }
            for ticket in serializer.data
        ]

        return Response(
            {
                "msg": "Tickets fetched successfully",
                "data": fields
            },
      
        )



# ticket info
class ShowTicketDetails(ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        ticket_id = request.data.get("ticket_id")

        if not ticket_id:
            return Response(
                {"msg": "ticket_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"msg": "Ticket not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TicketSerializer(ticket)

        data = {
            "name": serializer.data["name"],
            "event": serializer.data["event"],
            "event_id": serializer.data["event"],
            "event_title": serializer.data["event_title"],
            "price": serializer.data["price"],
            "benefits": serializer.data["benefits"],
            "available_seats": serializer.data["available_seats"],
            "discount": serializer.data.get("discount",0.0) , #["discount"],
            "tax":serializer.data.get("tax",0.0) ,
        }

        return Response(
            {
                "msg": "Ticket details fetched successfully",
                "data": data
            },
            status=status.HTTP_200_OK
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

        if Booking.objects.filter(event_id=event_id,ticket_id=ticket_id,
                                  payment_status__in=["paid","reserved"],
                                  created_by=user).exists():
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
            raise ValidationError("selected_seats must be greater than zero.")

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
            expires_at = timezone.now() + timedelta(hours=1)  # expires after 1 hour
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
                                                booking.id
                                            )
    
        return Response(
            {
                "message": f"Booking successful. The payment link has been sent to your registered email address: {user.email}",
                "event":booking.event.title,
                "booking_id": booking.id,
                "amount": booking.amount,
                "payment_status": booking.payment_status,
            },)

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
        

# =======================================UI======================================= #

@login_not_required
def payment_page(request):
    print("payment_page")
    booking_id = request.GET.get("booking_id")
    booking = get_object_or_404(
        Booking.objects.select_related(
            "event",
            "ticket",
            "created_by",
        ),
        id=booking_id,
    )

    context = {
        "booking_id": booking.id,
        "event": booking.event.title,
        "ticket_name": booking.ticket.name,
        "seats": booking.selected_seats,
        "ticket_price": float(booking.ticket.price),
        "discount": float(booking.ticket.discount or 0),
        "tax": float(booking.ticket.tax or 0),
        "total_amount": float(booking.amount),
        "payment_status": booking.payment_status,
        # ADD THIS
        "first_name": booking.created_by.first_name,
        "email": booking.created_by.email,
    }

    return render(
        request,
        "logic/payment.html",
        {
            "context": context,
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_payment_order(request):
    print("create_payment_order")
    booking_id = request.data.get("booking_id")
    if not booking_id:
        return Response(
            {"error": "booking_id is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    booking = get_object_or_404(Booking,  id=booking_id )

    # Check booking status
    if booking.payment_status != "reserved":
        return Response(
            {
                "error": "This booking is not available for payment.",
                "payment_status": booking.payment_status,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check whether booking has expired
    if booking.expires_at and timezone.now() >= booking.expires_at:
        booking.payment_status = "expired"
        booking.save(update_fields=["payment_status"])

        return Response(
            {"error": "This booking has expired."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Razorpay amount must be in paise
    amount_in_paise = int(booking.amount * Decimal("100"))
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    razorpay_order = client.order.create(
        {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": str(booking.id),
        }
    )

    # Save Razorpay order ID
    booking.razorpay_order_id = razorpay_order["id"]
    booking.save(update_fields=["razorpay_order_id"])

    return Response(
        {
            "booking_id": booking.id,
            "order_id": razorpay_order["id"],
            "amount": amount_in_paise,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_payment(request):
    print("verify_payment")
    booking_id = request.data.get("booking_id")
    payment_id = request.data.get("razorpay_payment_id")
    order_id = request.data.get("razorpay_order_id")
    signature = request.data.get("razorpay_signature" )
    if not all([booking_id, payment_id, order_id, signature, ]):
        return Response({"error": "Payment verification data is incomplete." },status=status.HTTP_400_BAD_REQUEST )
    booking = get_object_or_404(Booking, id=booking_id)

    # Make sure this order belongs to this booking
    if booking.razorpay_order_id != order_id:
        return Response({ "error": "Invalid Razorpay order."},
            status=status.HTTP_400_BAD_REQUEST
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })

    except razorpay.errors.SignatureVerificationError:
        booking.payment_status = "failed"
        booking.save(update_fields=["payment_status" ])

        return Response({"error":"Payment verification failed."
            }, status=status.HTTP_400_BAD_REQUEST)

    # Payment successfully verified
    booking.payment_status = "paid"
    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature

    booking.save(
        update_fields=[
            "payment_status",
            "razorpay_payment_id",
            "razorpay_signature",
        ])

    # Generate PDF ticket and email it
    generate_ticket.delay(booking.id)
    return Response(
        {
            "message": "Payment verified successfully.",
            "booking_id":  booking.id,
            "payment_status": booking.payment_status,
        },
        status=status.HTTP_200_OK
    )














