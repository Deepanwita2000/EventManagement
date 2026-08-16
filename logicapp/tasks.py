# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from logicapp.models import Booking, EventTicket,Event





@shared_task
def send_booking_failed_email(user_email, first_name, event_title):
    print("send_booking_failed_email()......")
    subject = "Booking Expired"
    print(subject)

    message = f"""
Hi {first_name},

Your reservation for the event "{event_title}" has expired because the payment was not completed within 1 hour.

The reserved seats have now been released and are available for booking again.

If you still wish to attend the event, please visit the application and make a new booking.

Thank you.

Regards,
Event Management Team
"""
    print(message)
    print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
    print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)
    print("Sending to:", user_email)
    

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )

@shared_task
def expire_bookings():
    print("calling expire_bookings(),,......")

    bookings = Booking.objects.filter(payment_status="reserved",     expires_at__lte=timezone.now())

    for booking in bookings:
        with transaction.atomic():

            ticket = booking.ticket

            ticket.available_seats += booking.selected_seats
            ticket.save()

            booking.payment_status = "expired"
            booking.save()

            send_booking_failed_email.delay(
                booking.created_by.email,
                booking.created_by.first_name,
                booking.event.title,
            )






@shared_task
def send_booking_confirmation_email(
    user_email,
    first_name,
    event_title,
    ticket_name,
    seats,
    amount,
):
    print("send_booking_confirmation_email()....")
    subject = "Booking Reserved"
    print(subject)

    message = f"""
Hi {first_name},

Your booking request has been received.

Event : {event_title}
Ticket : {ticket_name}
Seats  : {seats}
Amount : ₹{amount}

Your seats are reserved for the next 1 hour.

Please complete your payment before the reservation expires.

Regards,
Event Management Team
"""
    print(message)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )



# logicapp/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_payment_success_email(
    user_email,
    first_name,
    event_title,
    ticket_name,
    seats,
    amount,
):
    print("send_payment_success_email()....")
    subject = "Payment Successful"
    print(subject)

    message = f"""
Hi {first_name},

Your payment has been received successfully.

Booking Details:
------------------------
Event : {event_title}
Ticket : {ticket_name}
Seats  : {seats}
Amount : ₹{amount}

Your booking is now confirmed.

Thank you for choosing our Event Management platform.

Regards,
Event Management Team
"""
    print(message)
    

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )








#////////////////////////////////////////////////////// ticket generation



import uuid
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from logicapp.models import Booking, EventTicket
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def generate_ticket(booking_id):
    print("generate_ticket()....")

    booking = Booking.objects.select_related(
        "event",
        "ticket",
        "created_by",
    ).get(id=booking_id)

    ticket_number = "EVT-" + uuid.uuid4().hex[:10].upper()

    event_ticket = EventTicket.objects.create(
        booking=booking,
        ticket_number=ticket_number,
    )

    # update public_count udner Event model
    event=booking.event
    event.public_count += booking.selected_seats
    event.save(update_fields=["public_count"])


    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b><font size=20>EVENT MANAGEMENT SYSTEM</font></b>",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            f"<b>Ticket Number:</b> {ticket_number}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Booked By:</b> {booking.created_by.first_name} {booking.created_by.last_name}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Email:</b> {booking.created_by.email}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            f"<b>Event:</b> {booking.event.title}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Ticket Type:</b> {booking.ticket.name}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Number of Seats:</b> {booking.selected_seats}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Amount:</b> ₹ {booking.amount}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            "<b>Payment Status:</b> PAID",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "Please carry this ticket while attending the event.",
            styles["Italic"],
        )
    )

    elements.append(
        Paragraph(
            "This ticket is generated automatically.",
            styles["Italic"],
        )
    )

    doc.build(elements)

    # event_ticket.pdf.save(
    #     f"{ticket_number}.pdf",
    #     ContentFile(pdf_buffer.getvalue()),
    #     save=False,
    # )

    # event_ticket.save()
    event_ticket.pdf.save(
    f"{ticket_number}.pdf",
    ContentFile(pdf_buffer.getvalue()),
    save=False,
)

    event_ticket.save()
    subject = "Your Event Ticket"

    message = f"""
    Hi {booking.created_by.first_name},

    Your payment has been received successfully.

    Event : {booking.event.title}

    Ticket : {booking.ticket.name}

    Seats : {booking.selected_seats}

    Amount : ₹{booking.amount}

    Ticket Number : {ticket_number}

    Please find your ticket attached.

    Thank you.
    """

    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [booking.created_by.email],
    )

    email.attach_file(event_ticket.pdf.path)

    email.send()

    # return f"{ticket_number} generated successfully."